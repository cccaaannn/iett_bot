from iett_bot import iett_bot
from extprint import printlist



driver_path = "C:\\Users\\can\\ProjectDependencies\\driver\\chromedriver.exe"
iett_bot = iett_bot(driver_path, options=["--headless","--no-sandbox","--disable-dev-shm-usage"])

iett_bot.set_stop("besiktas_bahcesehir_universitesi")
bus_30d = iett_bot.find_me_buses("30d")
bus_dt1 = iett_bot.find_me_buses("dt1")

printlist(bus_30d,color="GREEN")
printlist(bus_dt1,color="BLUE")
