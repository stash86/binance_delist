# scanner.py
import requests
from requests.exceptions import RequestException
# import bot_control
from bs4 import BeautifulSoup


def get_delist_tokens():
    tokens = []
    try:
        req = requests.get("https://www.binance.com/en/support/announcement/delisting?c=161&navId=161")
        soup = BeautifulSoup(req.content, 'html.parser')
        #news = req.json()
        links = soup.find_all('a')
        for link in links:
            if link:
                print(link.get('href'))
            #title = article["title"].lower()
            #match_result = title.match("binance will delist (.*) on (.*)")
            #if match_result:
            #    article_tokens = match_result.group(1).split(",|&")
            #    tokens.extend(map(lambda elem: elem.strip(), article_tokens))
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
    get_delist_tokens()