## iett bot

- **pulls bus times from iett site using requests or selenium**
- **mail example for receiving bus times as mail**
- **telegram example for receiving bus times as telegram message** 


## using requests
```python
from iett_bot_requests import iett_bot_requests
iett_bot = iett_bot_requests()
```
## using selenium
```python
from iett_bot_selenium import iett_bot_selenium
driver_path = "Users/can/ProjectDependencies/driver/chromedriver.exe"
iett_bot = iett_bot_selenium(driver_path, options=["--headless","--no-sandbox","--disable-dev-shm-usage"])
```

## bot example example
```python
# add a new stop
iett_bot.add_stop("home","114051")
stops = iett_bot.get_stops()
print(stops)

# set the stop
iett_bot.set_stop("home")
dt2 = iett_bot.find_me_buses("dt2")
print(dt2)
```
## get all buses
```python
buses = iett_bot.give_me_all_buses()
```


