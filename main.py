import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  


path = "C:\\Users\\can\\ProjectDependencies\\driver\\chromedriver.exe"



class bot():
    def __init__(self,driver_path, options = ["--headless"]):
        self.driver_path = driver_path
        self.options =options

        self.init_driver(self.driver_path, self.options)
        

    def init_driver(self,driver_path, options):
        self.set_driver_options(options)
        self.driver = webdriver.Chrome(executable_path=driver_path, options=self.chrome_options)

    def set_driver_options(self,options):
        self.chrome_options = Options()  
        if(options):
            for option in options:
                self.chrome_options.add_argument(option)
        
    def get_url(self, url):
        self.driver.get(url)

    def get_trs(self):
        body = self.driver.find_element_by_tag_name("tbody")
        trs = body.find_elements_by_tag_name("tr")
        return trs

    def find_me_bus(self, bus_code):
        bus_code = bus_code.lower()

        body = self.driver.find_element_by_tag_name("tbody")
        trs = body.find_elements_by_tag_name("tr")
        buses = []
        for tr in trs:
            found_buss_code = tr.find_element_by_tag_name("mark").text.lower()
            if(found_buss_code == bus_code):
                arriving_time = tr.find_element_by_class_name("varissaati").text
                remaining_time = tr.find_element_by_class_name("td_LineEstimated").text[8:]
                bus = {"bus code":found_buss_code,"arriving time":arriving_time,"remaining time":remaining_time}
                buses.append(bus)
                print("!!!buss found!!!")

        return buses
        


bot = bot(path,options=["--headless","--no-sandbox","--disable-dev-shm-usage"])
bot.get_url("https://www.iett.istanbul/tr/main/duraklar/114962/BE%C5%9E%C4%B0KTA%C5%9E%20B.%C3%9CN%C4%B0VERS%C4%B0T-%C4%B0ETT-Duraktan-Ge%C3%A7en-Hatlar-Durak-Bilgileri-Hatt%C4%B1n-Duraktan-Ge%C3%A7i%C5%9F-Saatleri")

bus_30d = bot.find_me_bus("30d")
bus_dt1 = bot.find_me_bus("dt1")

from extprint import printlist

printlist(bus_30d)
printlist(bus_dt1)



