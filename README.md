# binance_delist

Scrape binance web for delisting announcement and send API call to specified bots to blacklist them

``` 
bash install_chrome.sh
cp bots.json.example bots.json
```

* Modify bots.json with the info of your bots
* Modify blacklist.json to become initial blacklist for all the bots. You can use `blacklist.json.example` if you prefer no initial blacklist.
* Modify `loop_secs` to suit your preference of how often the bot scrape binance. Default is 90 seconds.

## Non-docker
```
bash install.sh
source .venv/bin/activate
bash run.sh
```


## Docker
```
docker-compose up -d --build
```