from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

url = "https://www.binance.com/en/support/announcement/delisting?c=161&navId=161"

def get_delist_tokens(url):
	tokens = []
	try:
		options = Options()
		options.add_argument('--headless')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		options.add_argument('--remote-debugging-pipe')
		driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

		driver.get(url)

		html_source = driver.page_source

		soup = BeautifulSoup(html_source, "html.parser")

		driver.quit()

		links = soup.find_all('a')
		for link in links:
			if link:
				# print(link.get('href'))
				# print(link.text)
				title = link.text.upper()
				if "BINANCE WILL DELIST " in title:
					title = title.replace("BINANCE WILL DELIST ", '')
					arr_title = title.split(" ON ")
					arr_coins = arr_title[0].split(", ")
					for coin in arr_coins:
						blacklist = f"${coin}/.*"
						if not blacklist in tokens:
							tokens.append(blacklist)
					# article_tokens = match_result.group(1).split(",|&")
					# tokens.extend(map(lambda elem: elem.strip(), article_tokens))

		print(tokens)
	except RequestException as e:
		print("Failed to get article list.")
		print(e)
	return tokens

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
	get_delist_tokens(url)