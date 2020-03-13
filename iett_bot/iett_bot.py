import time
import json

class iett_bot():

    base_url = "https://www.iett.istanbul/tr/main/duraklar/"

    def __init__(self):
        self.__load_stops()
        
    def __read_cfg_file(self, cfg_path="iett_bot/cfg/stops.cfg"):
        try:
            with open(cfg_path,"r") as file:
                dict = json.load(file)
            return dict
        except:
            return 0
    
    def __write_cfg_file(self, cfg_path="iett_bot/cfg/stops.cfg"):
        try:
            with open(cfg_path,"w") as file:
                json.dump(self.stops, file)
        except:
            pass


    def __load_stops(self):
        self.stops = self.__read_cfg_file()
        if(not self.stops):
            print("file read error (stops.cfg), default values are assigned")
            self.stops = {"dereboyu_sehit_batuhan_ergin":"114051","besiktas_bahcesehir_universitesi":"114962"}
        self.set_stop(list(self.stops.keys())[0])


    def bus_dict_to_str(self, buses):
        str_buses = buses[0]["stop name"] + "\n"
        for index, bus in enumerate(buses):
            str_buses += "{0} -> {1} {2} {3}\n".format(index, bus["bus code"], bus["arriving time"], bus["remaining time"] )
        return str_buses

    def is_stop_exist(self, stop_name):
        if(stop_name in self.stops):
            return True
        else:
            return False

    def get_stops(self):
        return self.stops

    def add_stop(self, stop_name, stop_code, allow_everride=True):
        if(allow_everride):
            temp_dict = {stop_name:stop_code}
            self.stops.update(temp_dict)
            self.__write_cfg_file()
        else:
            if(not self.is_stop_exist(stop_name)):
                temp_dict = {stop_name:stop_code}
                self.stops.update(temp_dict)
                self.__write_cfg_file()

    def del_stop(self, stop_name):
        if(stop_name in self.stops):
            self.stops.pop(stop_name)
            self.__write_cfg_file()
        else:
            print("can't delete it is not in th dict")

    def set_stop(self, stop_name):
        if(self.stops[stop_name]):
            self.current_stop = stop_name
            self.stop_url = self.base_url + self.stops[stop_name]
        else:
            print("stop is not exists")

    
