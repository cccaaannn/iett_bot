FROM python:3

ADD iett_bot /

RUN pip3 install -r requirements.txt

CMD [ "python", "./iett_bot/telegram_example/telegrambot.py.py" ]