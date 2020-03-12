from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from my_bot_key import botkey
# from iett_bot import iett_bot
import sys
sys.path.append(".")
from iett_bot.iett_bot import iett_bot



def __set_logger(logger_name, log_file, verbose):
    import logging

    logger = logging.getLogger(logger_name)  

    # .hasHandlers() is not working 
    # print(logger.handlers)
    # print(logger.hasHandlers())
    # if logger exists don't add new handlers
    if(not logger.handlers):
        verbosity = {0:50,1:40,2:30,3:20}
        if(verbosity.get(verbose)):
            logger.setLevel(verbosity.get(verbose))
        else:
            logger.setLevel(20)
        
        # log formatter
        formatter = logging.Formatter("[%(levelname)s] %(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        # file handler
        if(log_file):
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger



def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("""usage 
    /bus <bus name> or /bus <bus name> <stop name>
    /addstop <stop name> <stop code>
    /delstop <stop name>
    /showstops
    /help
    """)

    # log info
    logger.info("help used username:{0}".format(update.message.from_user.username))


def error(update, context):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)



def bus(update, context):
    try:
        if(iett_bot.is_stop_exist(context.args[1])):
            iett_bot.set_stop(context.args[1])
            update.message.reply_text("I am tying to find buses for {0}".format(context.args[1]))
        else:
            update.message.reply_text("'{0}' this stop is not exists \nyou can add stops with /addstop <stop name> <stop code>".format(context.args[1]))
            return

        if(context.args[0] == "all"):
            buses = iett_bot.give_me_all_buses()
        else:
            buses = iett_bot.find_me_buses(context.args[0])
        
        if(buses):
            buses_str = iett_bot.bus_dict_to_str(buses)
            update.message.reply_text(buses_str)
        else:
            update.message.reply_text("I couldn't find any {0} on stop {1}".format(context.args[0],context.args[1]))

        # log info
        logger.info("buses listed {0} username:{1}".format(context.args[0],update.message.from_user.username))
    except (IndexError, ValueError):
        update.message.reply_text("usage /bus <bus name> <stop name> \nto list all the buses for a stop /bus all <stop name>")

        # log info
        logger.warning("function bus username:{0}".format(update.message.from_user.username), exc_info=True)
    except:
        update.message.reply_text("most likely you broke something")

        # log info
        logger.error("function bus username:{0}".format(update.message.from_user.username), exc_info=True)


def add_stop(update, context):
    try:
        iett_bot.add_stop(context.args[0], context.args[1])
        update.message.reply_text("stop added")

        # log info
        logger.info("stop added {0} username:{1}".format(context.args[0],update.message.from_user.username))
    except (IndexError, ValueError): 
        update.message.reply_text("usage /add_stop <stop name> <stop code>")

        # log info
        logger.warning("function add_stop username:{0}".format(update.message.from_user.username), exc_info=True)

def del_stop(update, context):
    try:
        iett_bot.del_stop(context.args[0])
        update.message.reply_text("stop deleted")

        # log info
        logger.info("stop deleted {0} username:{1}".format(context.args[0], update.message.from_user.username))
    except (IndexError, ValueError): 
        update.message.reply_text("usage /del_stop <stop name>")

        # log info
        logger.warning("function del_stop username:{0}".format(update.message.from_user.username), exc_info=True)

def show_stops(update, context):
    update.message.reply_text(iett_bot.get_stops())
    # log info
    logger.info("stops listed username:{0}".format(update.message.from_user.username))
    
def hop(update, context):
    update.message.reply_text("hi")



driver_path = "C:\\Users\\can\\ProjectDependencies\\driver\\chromedriver.exe"
iett_bot = iett_bot(driver_path, options=["--headless","--no-sandbox","--disable-dev-shm-usage"])

logger = __set_logger(__name__, "iett_bot/telegram_example/log/telegram.log", 3)


updater = Updater(botkey, use_context=True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("bus", bus, pass_args=True))
dp.add_handler(CommandHandler("addstop", add_stop, pass_args=True))
dp.add_handler(CommandHandler("delstop", del_stop, pass_args=True))
dp.add_handler(CommandHandler("showstops", show_stops))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("hop", hop))


dp.add_error_handler(error)

updater.start_polling()
updater.idle()





