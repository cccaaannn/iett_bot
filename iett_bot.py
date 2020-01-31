import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  


class iett_bot:
    def __init__(self,driver_path, options = ["--headless"]):
        self.driver_path = driver_path
        self.options = options

        self.base_url = "https://www.iett.istanbul/tr/main/duraklar/"

        self.__load_stops()
        self.__init_driver(self.driver_path, self.options)
        
        
    def __init_driver(self,driver_path, options):
        self.__set_driver_options(options)
        self.driver = webdriver.Chrome(executable_path=driver_path, options=self.chrome_options)

    def __set_driver_options(self,options):
        self.chrome_options = Options()  
        if(options):
            for option in options:
                self.chrome_options.add_argument(option)
        
    def __get_url(self, url):
        self.driver.get(url)
        
    def __read_cfg_file(self,cfg_path="stops.cfg"):
        try:
            with open(cfg_path,"r") as file:
                dict = json.load(file)
            return dict
        except:
            return 0

    def __load_stops(self):
        self.stops = self.__read_cfg_file()
        if(not self.stops):
            print("file read error stops.cfg default values are assigned")
            self.stops = {"dereboyu_sehit_batuhan_ergin":"114051","besiktas_bahcesehir_universitesi":"114962"}
        self.set_stop(list(self.stops.keys())[0])



    def get_stops(self):
        return self.stops

    def set_stop(self, stop_name):
        if(self.stops[stop_name]):
            self.current_stop = stop_name
            self.stop_url = self.base_url + self.stops[stop_name]
        else:
            print("stop is not exists")

    def find_me_buses(self, bus_code):
        self.__get_url(self.stop_url)

        bus_code = bus_code.lower()

        body = self.driver.find_element_by_tag_name("tbody")
        trs = body.find_elements_by_tag_name("tr")
        buses = []
        for tr in trs:
            found_buss_code = tr.find_element_by_tag_name("mark").text.lower()
            if(found_buss_code == bus_code):
                arriving_time = tr.find_element_by_class_name("varissaati").text
                remaining_time = tr.find_element_by_class_name("td_LineEstimated").text[8:]
                bus = {"stop name":self.current_stop,"stop code":self.stops[self.current_stop],"bus code":found_buss_code,"arriving time":arriving_time,"remaining time":remaining_time}
                buses.append(bus)
                print("!!!buss found!!!")

        return buses

    def give_me_all_buses(self):
        self.__get_url(self.stop_url)

        body = self.driver.find_element_by_tag_name("tbody")
        trs = body.find_elements_by_tag_name("tr")
        buses = []
        for tr in trs:
            found_buss_code = tr.find_element_by_tag_name("mark").text.lower()
            arriving_time = tr.find_element_by_class_name("varissaati").text
            remaining_time = tr.find_element_by_class_name("td_LineEstimated").text[8:]
            bus = {"stop name":self.current_stop,"stop code":self.stops[self.current_stop],"bus code":found_buss_code,"arriving time":arriving_time,"remaining time":remaining_time}
            buses.append(bus)
            print("!!!buss found!!!")

        return buses











