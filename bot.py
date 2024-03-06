from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
import rapidjson
from typing import Any, Dict, List, Optional
from pathlib import Path
from libs.api import FtRestClient
import logging

url = "https://www.binance.com/en/support/announcement/delisting?c=161&navId=161"
path_blacklist_file = 'blacklist.json'
path_processed_file = 'processed.json'
path_bots_file = 'bots.json'
CONFIG_PARSE_MODE = rapidjson.PM_COMMENTS | rapidjson.PM_TRAILING_COMMAS
tokens = []
has_been_processed = []
bots = []

loop_secs = 90

logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def get_delist_tokens(url, driver):
	class_p_list_coins = "css-zwb0rk"
	new_blacklist = []
	new_processed = []
	try:
		logger.info("Scrape delisting page")
		driver.get(url)

		html_source = driver.page_source

		soup = BeautifulSoup(html_source, "html.parser")

		links = soup.find_all("a")
		count_notice = 5;
		for link in links:
			title = link.text.upper()
			if title and (title not in has_been_processed) and (title not in new_processed):
				logger.info(f"New title : {title}")
				new_processed.append(title)
				if "BINANCE WILL DELIST " in title:
					title = title.replace("BINANCE WILL DELIST ", "")
					arr_title = title.split(" ON ")
					arr_coins = arr_title[0].split(", ")
					for coin in arr_coins:
						blacklist = f"{coin}/.*"
						if (not blacklist in tokens) and (not blacklist in new_blacklist):
							new_blacklist.append(blacklist)
				elif ("NOTICE OF REMOVAL OF " in title) and ("MARGIN" not in title) and (count_notice > 0):
					count_notice -= 1
					link = f"https://www.binance.com{link.get('href')}"
					driver.get(link)
					html_source = driver.page_source
					soup = BeautifulSoup(html_source, "html.parser")
					lis = soup.find_all("p", class_p_list_coins)
					for li in lis:
						spans = li.find_all("span", "richtext-text")
						for span in spans:
							if "/" in span.text:
								line = span.text.replace(":", "").strip()
								arr_coins = line.split(", ")
								for coin in arr_coins:
									coin = coin.strip()
									if (not coin in tokens[cur_exchange]) and (not coin in new_blacklist):
										new_blacklist.append(coin)

		driver.quit()
		
		if len(new_processed) > 0:
			has_been_processed.extend(new_processed)
			save_local_processed()

		if len(new_blacklist) > 0:
			tokens.extend(new_blacklist)
			save_local_blacklist()
			send_blacklist(new_blacklist)

	except Exception as e:
		logger.error("Failed to get article list.")
		logger.error(e)


def open_local_blacklist():

	try:
		logger.info("Loading local blacklist file")
		# Read config from stdin if requested in the options
		with Path(path_blacklist_file).open() if path_blacklist_file != '-' else sys.stdin as file:
			config = rapidjson.load(file, parse_mode=CONFIG_PARSE_MODE)
			for line in config['pair_blacklist']:
				tokens.append(line)
	except FileNotFoundError:
		raise OperationalException(
			f'Config file "{path_blacklist_file}" not found!'
			' Please create a config file or check whether it exists.')
	except rapidjson.JSONDecodeError as e:
		err_range = log_config_error_range(path_blacklist_file, str(e))
		raise OperationalException(
			f'{e}\n'
			f'Please verify the following segment of your configuration:\n{err_range}'
			if err_range else 'Please verify your configuration file for syntax errors.'
		)

	
def save_local_blacklist():
	logger.info("Saving local blacklist file")
	try:
		new_blacklist = dict()
		new_blacklist['pair_blacklist'] = tokens
		json_obj = rapidjson.dumps(new_blacklist)
		with open(path_blacklist_file, "w") as outfile:
			outfile.write(json_obj)
	except Exception as e:
		logger.info(e)


def open_local_processed():
	logger.info("Loading local processed file")
	try:
		# Read config from stdin if requested in the options
		with Path(path_processed_file).open() if path_processed_file != '-' else sys.stdin as file:
			config = rapidjson.load(file, parse_mode=CONFIG_PARSE_MODE)
			for line in config['processed']:
				has_been_processed.append(line)
	except FileNotFoundError:
		raise OperationalException(
			f'Config file "{path_processed_file}" not found!'
			' Please create a config file or check whether it exists.')
	except rapidjson.JSONDecodeError as e:
		err_range = log_config_error_range(path_processed_file, str(e))
		raise OperationalException(
			f'{e}\n'
			f'Please verify the following segment of your configuration:\n{err_range}'
			if err_range else 'Please verify your configuration file for syntax errors.'
		)

	
def save_local_processed():
	logger.info("Saving local processed file")
	try:
		new_processed = dict()
		new_processed['processed'] = has_been_processed
		json_obj = rapidjson.dumps(new_processed)
		with open(path_processed_file, "w") as outfile:
			outfile.write(json_obj)
	except Exception as e:
		logger.info(e)


def load_bots_data():
	with Path(path_bots_file).open() if path_bots_file != '-' else sys.stdin as file:
		data_bots = rapidjson.load(file, parse_mode=CONFIG_PARSE_MODE)
		for line in data_bots:
			bots.append(line)


def send_blacklist(blacklist):
	if len(blacklist) > 0:
		for bot in bots:
			logger.info(f"Send blacklist list to {bot['ip_address']}")
			api_bot = FtRestClient(f"http://{bot['ip_address']}", bot['username'], bot['password'])
			for line in blacklist:
				api_bot.blacklist(line)


if __name__ == "__main__":
	load_bots_data()
	open_local_blacklist()
	send_blacklist(tokens)
	open_local_processed()

	starttime = time.monotonic()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--remote-debugging-pipe")
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
	while True:
		get_delist_tokens(url, driver)
		time.sleep(loop_secs - ((time.monotonic() - starttime) % loop_secs))