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

url = "https://www.binance.com/en/support/announcement/delisting?c=161&navId=161"
path_blacklist_file = 'blacklist.json'
path_processed_file = 'processed.json'
path_bots_file = 'bots.json'
CONFIG_PARSE_MODE = rapidjson.PM_COMMENTS | rapidjson.PM_TRAILING_COMMAS
tokens = []
has_been_processed = []
bots = []

def get_delist_tokens(url):
	class_p_list_coins = "css-zwb0rk"	
	try:
		options = Options()
		options.add_argument("--headless")
		options.add_argument("--no-sandbox")
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--remote-debugging-pipe")
		driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

		print("Scrape delisting page")
		driver.get(url)

		html_source = driver.page_source

		soup = BeautifulSoup(html_source, "html.parser")

		links = soup.find_all("a")
		count_notice = 5;
		for link in links:
			title = link.text.upper()
			if title and (title not in has_been_processed):
				print(title)
				has_been_processed.append(title)
				# print(link.get("href"))
				# print(link.text)
				if "BINANCE WILL DELIST " in title:
					title = title.replace("BINANCE WILL DELIST ", "")
					arr_title = title.split(" ON ")
					arr_coins = arr_title[0].split(", ")
					for coin in arr_coins:
						blacklist = f"{coin}/.*"
						if not blacklist in tokens:
							tokens.append(blacklist)
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
								line = span.text.replace(": ", "")
								arr_coins = line.split(", ")
								for coin in arr_coins:
									if not coin in tokens:
										tokens.append(coin)

		driver.quit()
		save_local_blacklist()
		save_local_processed()
	except Exception as e:
		print("Failed to get article list.")
		print(e)

def open_local_blacklist():

	try:
		print("Loading local blacklist file")
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
	print("Saving local blacklist file")
	try:
		new_blacklist = dict()
		new_blacklist['pair_blacklist'] = tokens
		json_obj = rapidjson.dumps(new_blacklist)
		with open(path_blacklist_file, "w") as outfile:
			outfile.write(json_obj)
	# except FileNotFoundError:
	# 	raise OperationalException(
	# 		f'Config file "{path}" not found!'
	# 		' Please create a config file or check whether it exists.')
	# except rapidjson.JSONDecodeError as e:
	# 	err_range = log_config_error_range(path, str(e))
	# 	raise OperationalException(
	# 		f'{e}\n'
	# 		f'Please verify the following segment of your configuration:\n{err_range}'
	# 		if err_range else 'Please verify your configuration file for syntax errors.'
	# 	)
	except Exception as e:
		print(e)
	
	# f = open(path_blacklist)
	
	# data = json.load(f)

	# f.close()

	# for i in data['exchange']['pair_blacklist']:
	# 	print(i)


def open_local_processed():
	print("Loading local processed file")
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
	print("Saving local processed file")
	try:
		new_processed = dict()
		new_processed['processed'] = has_been_processed
		json_obj = rapidjson.dumps(new_processed)
		with open(path_processed_file, "w") as outfile:
			outfile.write(json_obj)
	# except FileNotFoundError:
	# 	raise OperationalException(
	# 		f'Config file "{path}" not found!'
	# 		' Please create a config file or check whether it exists.')
	# except rapidjson.JSONDecodeError as e:
	# 	err_range = log_config_error_range(path, str(e))
	# 	raise OperationalException(
	# 		f'{e}\n'
	# 		f'Please verify the following segment of your configuration:\n{err_range}'
	# 		if err_range else 'Please verify your configuration file for syntax errors.'
	# 	)
	except Exception as e:
		print(e)
	
	# f = open(path_processed)
	
	# data = json.load(f)

	# f.close()

	# for i in data['exchange']['pair_processed']:
	# 	print(i)


def load_bots_data():
	with Path(path_bots_file).open() if path_bots_file != '-' else sys.stdin as file:
		data_bots = rapidjson.load(file, parse_mode=CONFIG_PARSE_MODE)
		for line in data_bots:
			bots.append(line)


def send_blacklist():
	for bot in bots:
		api_bot = FtRestClient(bot['ip_address'], bot['username'], bot['password'])
		print(api_bot.blacklist(tokens))

# def blacklist(bot_data, coin):
# 	print(api.profit(ip, days))

if __name__ == "__main__":
	load_bots_data()
	open_local_blacklist()
	send_blacklist()
	open_local_processed()
	get_delist_tokens(url)