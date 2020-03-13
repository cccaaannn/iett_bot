from extprint import printlist

from iett_bot_requests import iett_bot_requests
from iett_bot_selenium import iett_bot_selenium

# driver_path = "C:\\Users\\can\\ProjectDependencies\\driver\\chromedriver.exe"
# iett_bot = iett_bot_selenium(driver_path, options=["--headless","--no-sandbox","--disable-dev-shm-usage"])
iett_bot = iett_bot_requests()

iett_bot.set_stop("besiktas_bahcesehir_universitesi")
buses = iett_bot.give_me_all_buses()
printlist(buses)

bus_30d = iett_bot.find_me_buses("30m")
bus_dt1 = iett_bot.find_me_buses("dt1")

printlist(bus_30d,color="GREEN")
printlist(bus_dt1,color="BLUE")


# buses = iett_bot.give_me_all_buses()
# printlist(buses)

# iett_bot.add_stop("home","114051")
# iett_bot.get_stops()

# iett_bot.set_stop("home")
# bus = iett_bot.find_me_buses("dt2")



