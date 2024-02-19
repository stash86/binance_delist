from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

url = "https://www.binance.com/en/support/announcement/delisting?c=161&navId=161"

def get_delist_tokens(url):
	class_p_list_coins = "css-zwb0rk"
	tokens = []
	has_been_processed = []
	try:
		options = Options()
		options.add_argument("--headless")
		options.add_argument("--no-sandbox")
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--remote-debugging-pipe")
		driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

		driver.get(url)

		html_source = driver.page_source

		soup = BeautifulSoup(html_source, "html.parser")

		links = soup.find_all("a")
		count_notice = 5;
		for link in links:
			if link and (link not in has_been_processed):
				has_been_processed.append(link)
				# print(link.get("href"))
				# print(link.text)
				title = link.text.upper()
				if "BINANCE WILL DELIST " in title:
					title = title.replace("BINANCE WILL DELIST ", "")
					arr_title = title.split(" ON ")
					arr_coins = arr_title[0].split(", ")
					for coin in arr_coins:
						blacklist = f"{coin}/.*"
						if not blacklist in tokens:
							tokens.append(blacklist)
					# article_tokens = match_result.group(1).split(",|&")
					# tokens.extend(map(lambda elem: elem.strip(), article_tokens))
				elif ("NOTICE OF REMOVAL OF " in title) and ("MARGIN" not in title) and (count_notice > 0):
					count_notice -= 1
					link = f"https://www.binance.com{link.get('href')}"
					driver.get(link)
					html_source = driver.page_source
					soup = BeautifulSoup(html_source, "html.parser")
					lis = soup.find_all("p", class_p_list_coins)
					for li in lis:
						spans = li.find_all("span", "richtext-text")
						exclude_in_span = ["<i>", "<strong>"]
						for span in spans:
							if "/" in span.text:
								line = span.text.replace(": ", "")
								arr_coins = line.split(", ")
								for coin in arr_coins:
									if not coin in tokens:
										tokens.append(coin)
								# print(span.text)
					# title = title.replace("BINANCE WILL DELIST ", "")
					# arr_title = title.split(" ON ")
					# arr_coins = arr_title[0].split(", ")
					# for coin in arr_coins:
					# 	blacklist = f"{coin}/.*"
					# 	if not blacklist in tokens:
					# 		tokens.append(blacklist)

		driver.quit()
		print(tokens)
	except Exception as e:
		print("Failed to get article list.")
		print(e)
	return tokens

def open_local_blacklist():
	f = open('blacklist.json')
	data = json.load(f)

	for i in data['exchange']['pair_blacklist']:
    	print(i)

def loop():
	print("Checking for delisted tokens...")
	blacklisted_tokens = []
	tokens = get_delist_tokens()
	# for instance in bot_control.instances:
	#     blacklist = bot_control.get_blacklist(instance)
	#     if not blacklist:
	#         continue
	#     tokens_not_blacklisted = [
	#         token
	#         for token in tokens
	#         if not any(bl_pair.split("/")[0].upper() == token for bl_pair in blacklist)
	#     ]
	#     for token in tokens_not_blacklisted:
	#         bot_control.blacklist_pair(instance, f"{token}/.*")
	#         blacklisted_tokens.append(token)
	# blacklisted_tokens = list(set(blacklisted_tokens))
	# if blacklisted_tokens:
	#     print(f"Blacklisted {len(blacklisted_tokens)} tokens.")

if __name__ == "__main__":
	open_local_blacklist()
	# get_delist_tokens(url)