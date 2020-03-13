from bs4 import BeautifulSoup
import requests
from iett_bot import iett_bot


class iett_bot_requests(iett_bot):
    def __init__(self):
        super().__init__()
        
        self.soup = BeautifulSoup(features="html.parser")
        

    def __get_url(self, url):
        raw_site = requests.get(url, verify=False).text
        self.soup = BeautifulSoup(raw_site, features="html.parser")



    def find_me_buses(self, bus_code):
        try:
            self.__get_url(self.stop_url)
            bus_code = bus_code.lower()

            body = self.soup.find("tbody")            
            trs = body.findAll("tr")
        
            buses = []
            for tr in trs:
                found_buss_code = tr.find("mark").text.lower()
                if(found_buss_code == bus_code):
                    arriving_time = tr.find("span", {"class": "varissaati"}).text
                    remaining_time = tr.find("td", {"class": "td_LineEstimated"}).text[8:]
                    bus = {"stop name":self.current_stop,"bus code":found_buss_code,"arriving time":arriving_time,"remaining time":remaining_time}
                    buses.append(bus)
                    print("!!!buss found!!!")

            return buses
        except:
            return ""

    def give_me_all_buses(self):
        try:
            self.__get_url(self.stop_url)

            body = self.soup.find("tbody")
            trs = body.findAll("tr")
        
            buses = []
            for tr in trs:
                found_buss_code = tr.find("mark").text.lower()
                arriving_time = tr.find("span", {"class": "varissaati"}).text                    
                remaining_time = tr.find("td", {"class": "td_LineEstimated"}).text[8:]
                bus = {"stop name":self.current_stop,"bus code":found_buss_code,"arriving time":arriving_time,"remaining time":remaining_time}
                buses.append(bus)
                print("!!!buss found!!!")

            return buses
        except:
            return ""
    