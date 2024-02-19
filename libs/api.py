import json
import requests
# from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
from urllib.parse import urlencode, urlparse, urlunparse
from typing import Optional

class API_FT:

	def __init__(self, data) -> None:
		self._serverurl = data['ip_address']
		self._session = requests.Session()
		self._session.auth = (data['username'], data['password'])

	def _call(self, method:str = 'GET', command:str = 'ping', params: Optional[dict] = None, data=None, files=None):
		if str(method).upper() not in ('GET', 'POST', 'PUT', 'DELETE'):
			raise ValueError(f'invalid method <{method}>')

		basepath = f"{self._serverurl}/api/v1/{command}"

		hd = {"Accept": "application/json",
			  "Content-Type": "application/json"
			  }

		# Split url
		schema, netloc, path, par, query, fragment = urlparse(basepath)
		# URLEncode query string
		query = urlencode(params) if params else ""
		# recombine url
		url = urlunparse((schema, netloc, path, par, query, fragment))

		try:
			resp = self._session.request(method, url, headers=hd, data=json.dumps(data))
			# return resp.text
			return resp.json()
		except ConnectionError:
			logger.warning("Connection error")
		
		# ip_address = self._ip
		# username = self._username
		# password = self._password
		# data = None

		# if (not(username == '')) and (not(password == '')):
		# 	basic = HTTPBasicAuth(username, password)
		# 	url = f"http://{ip_address}/api/v1/{command}"
			
		# 	if method == 'GET':
		# 		r = requests.get(url, auth=basic, params=params)
		# 	elif method == 'POST':
		# 		r = requests.post(url, auth=basic, data=params)

		# 	data = r.text

		# return data

	def _get(self, command, params: Optional[dict] = None):
		return self._call("GET", command, params=params)

	def _delete(self, command, params: Optional[dict] = None):
		return self._call("DELETE", command, params=params)

	def _post(self, command, params: Optional[dict] = None, data: Optional[dict] = None):
		return self._call("POST", command, params=params, data=data)

	def blacklist(self, *args):
        """Show the current blacklist.

        :param add: List of coins to add (example: "BNB/BTC")
        :return: json object
        """
        if not args:
            return self._get("blacklist")
        else:
            return self._post("blacklist", data={"blacklist": args})


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

