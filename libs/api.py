import json
import requests
from requests.auth import HTTPBasicAuth

class API_FT:

	def __init__(self, data) -> None:
		self._ip = data['ip_address']
		self._username = data['username']
		self._password = data['password']

	def call(self, method:str = 'GET', command:str = 'ping', params={}):
		ip_address = self._ip
		username = self._username
		password = self._password
		data = None

		if (not(username == '')) and (not(password == '')):
			basic = HTTPBasicAuth(username, password)
			url = f"http://{ip_address}/api/v1/{command}"
			
			if method == 'GET':
				r = requests.get(url, auth=basic, params=params)
			elif method == 'POST':
				r = requests.post(url, auth=basic)

			data = r.text

		return data


	def blacklist_post(self, pairs:list = []):
		params = {
			'blacklist': pairs
		}
		res = self.call(method="POST", command="blacklist_post", params=params)
		return res


# def forceenter(ip_address: str, pair: str, direction: str, rate: float):
# 	username, password = get_credentials(ip_address)

# 	if (not(username == '')) and (not(password == '')):
# 		params = {
# 			'pair': pair,
# 			'side': direction
# 		}

# 		if (rate > 0):
# 			params['price'] = rate
# 		res = call(ip_address, method='POST', command='forceenter', params=params)
# 		return res


# def forceexit(ip_address: str, trade_id:int = 0):
# 	username, password = get_credentials(ip_address)

# 	if (not(username == '')) and (not(password == '')):
# 		params = {'tradeid': (trade_id if trade_id > 0 else 'all')}
# 		res = call(ip_address, method='POST', command='forceexit', params=params)
# 		return res


# def logs(ip_address: str, limit:int = 50):
# 	username, password = get_credentials(ip_address)

# 	if (not(username == '')) and (not(password == '')):
# 		params = {}
# 		if limit > 0:
# 			params = {'limit': limit}
# 		res = call(ip_address, command='logs', params=params)
# 		return res


# def profit(ip_address: str, days:int = 0):
# 	username, password = get_credentials(ip_address)

# 	if (not(username == '')) and (not(password == '')):
# 		params = {}
# 		if days > 0:
# 			params = {'timescale': days}
# 		res = call(ip_address, command='profit', params=params)
# 		return res


# def start(ip_address: str):
# 	username, password = get_credentials(ip_address)

# 	if (not(username == '')) and (not(password == '')):
# 		res = call(ip_address, method='POST', command='start')
# 		return res


# def stop(ip_address: str):
# 	username, password = get_credentials(ip_address)

# 	if (not(username == '')) and (not(password == '')):
# 		res = call(ip_address, method='POST', command='stop')
# 		return res

