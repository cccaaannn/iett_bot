import datetime
from time import sleep
import getpass

from mail_functions import send_mail, receive_mail
from iett_bot import iett_bot



# set up mail stuff
automail_username = ""
automail_password = getpass.getpass()

server_incoming = "imap.gmail.com"
server_outgoing = "smtp.gmail.com"

receiver_mail = ""


driver_path = "C:\\Users\\can\\ProjectDependencies\\driver\\chromedriver.exe"

iett_bot = iett_bot(driver_path, options=["--headless","--no-sandbox","--disable-dev-shm-usage"])



def list_to_str(buses):
    str_buses = buses[0]["stop name"] + "\n\n"
    for index, bus in enumerate(buses):
        str_buses += "{0} -> {1} {2} {3}\n".format(index, bus["bus code"], bus["arriving time"], bus["remaining time"] )
    return str_buses



# set up parameters
remind_hour = 5
remind_minute = 30 
waiting_interval = 10
send_flag = False
while(True):
    
    # ---------------------------send daily reminder mail and delete temps--------------------------------------------
    now = datetime.datetime.now()
    time_to_send = now.replace(hour=remind_hour, minute=remind_minute, second=0, microsecond=0)
    # print(now)

    if(now > time_to_send and not send_flag):
        send_flag = True

        subject = "bus times " + datetime.datetime.strftime(now,"%d/%m/%y")

        iett_bot.set_stop("dereboyu_sehit_batuhan_ergin")
        bus_30d = iett_bot.find_me_buses("30d")
        bus_dt2 = iett_bot.find_me_buses("dt2")
        buses = bus_dt2 + bus_30d
        str_buses = list_to_str(buses)

        send_mail(server_incoming, automail_username, automail_password, receiver_mail, subject, str_buses)

    elif(time_to_send > now):
        send_flag = False
        subject = ""
    
    # -------------------------------------------------------------------------------------------------------------


    # ---------------------------check mailbox for commands---------------------------------------------------------

    result, subject, sender = receive_mail(server_outgoing, automail_username, automail_password)
    
    if(result and receiver_mail in sender):
        if(subject == "evdeyim"):
            iett_bot.set_stop("dereboyu_sehit_batuhan_ergin")
            bus_30d = iett_bot.find_me_buses("30d")
            bus_dt2 = iett_bot.find_me_buses("dt2")
            buses = bus_dt2 + bus_30d
            str_buses = list_to_str(buses)

            send_mail(server_incoming, automail_username, automail_password, receiver_mail, "buses", str_buses)
        
        elif(subject == "okuldayim"):
            iett_bot.set_stop("besiktas_bahcesehir_universitesi")
            bus_30d = iett_bot.find_me_buses("30d")
            bus_dt1 = iett_bot.find_me_buses("dt1")   
            buses = bus_dt1 + bus_30d
            str_buses = list_to_str(buses)
            send_mail(server_incoming, automail_username, automail_password, receiver_mail, "buses", str_buses)
        
        elif(subject == "all_buses"):
            iett_bot.set_stop("besiktas_bahcesehir_universitesi")
            all_buses = iett_bot.give_me_all_buses()
            str_buses = list_to_str(all_buses)
            send_mail(server_incoming, automail_username, automail_password, receiver_mail, "all buses", str_buses)
        

        elif(subject == "info"):
            subject = "commands\nevdeyim okuldayim info time:"
            send_mail(server_incoming, automail_username, automail_password, receiver_mail, "all commands", subject)
        

        elif(subject[0:5] == "time:"):
            try:
                new_reminder_time = datetime.datetime.strptime(subject[5:], '%H:%M')
                subject = "reminder time changed to {}:{}".format(new_reminder_time.hour,new_reminder_time.minute)
                remind_hour = int(new_reminder_time.hour)
                remind_minute = int(new_reminder_time.minute)
                send_mail(server_incoming, automail_username, automail_password, receiver_mail, subject, "")
            except:
                subject = "command error"
                send_mail(server_incoming, automail_username, automail_password, receiver_mail, subject, "")

        else:
             send_mail(server_incoming, automail_username, automail_password, receiver_mail, "unknown command received", "")


        #check the mailbox until it is empty
        continue

    sleep(waiting_interval)

    # -------------------------------------------------------------------------------------------------------------


