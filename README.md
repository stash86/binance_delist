# binance_delist
``` 
bash install_chrome.sh
cp bots.json.example bots.json
```

* Modify bots.json with the info of your bots
* Modify blacklist.json to become initial blacklist for all the bots
* Modify `loop_secs` to suit your preference of how often the bot scrape binance. Default is 90 seconds.

## Non-docker
```
bash install.sh
source .venv/bin/activate
bash run.sh
```


## Docker
