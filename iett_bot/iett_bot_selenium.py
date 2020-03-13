from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from iett_bot import iett_bot


class iett_bot_selenium(iett_bot):
    
    def __init__(self, driver_path, options = ["--headless","--no-sandbox","--disable-dev-shm-usage"]):
        super().__init__()
        self.driver_path = driver_path
        self.options = options
        self.__init_driver(self.driver_path, self.options)

    def __init_driver(self,driver_path, options):
        self.__set_driver_options(options)
        self.driver = webdriver.Chrome(executable_path=driver_path, options=self.chrome_options)

    def __set_driver_options(self, options):
        self.chrome_options = Options()  
        if(options):
            for option in options:
                self.chrome_options.add_argument(option)
        
    def __get_url(self, url):
        self.driver.get(url)


    def find_me_buses(self, bus_code):
        try:
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
                    bus = {"stop name":self.current_stop,"bus code":found_buss_code,"arriving time":arriving_time,"remaining time":remaining_time}
                    buses.append(bus)
                    print("!!!buss found!!!")

            return buses
        except:
            return ""

    def give_me_all_buses(self):
        try:
            self.__get_url(self.stop_url)

            body = self.driver.find_element_by_tag_name("tbody")
            trs = body.find_elements_by_tag_name("tr")
            buses = []
            for tr in trs:
                found_buss_code = tr.find_element_by_tag_name("mark").text.lower()
                arriving_time = tr.find_element_by_class_name("varissaati").text
                remaining_time = tr.find_element_by_class_name("td_LineEstimated").text[8:]
                bus = {"stop name":self.current_stop,"bus code":found_buss_code,"arriving time":arriving_time,"remaining time":remaining_time}
                buses.append(bus)
                print("!!!buss found!!!")

            return buses
        except:
            return ""






