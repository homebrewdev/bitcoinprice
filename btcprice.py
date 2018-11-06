import requests
from datetime import datetime
import telebot
import config
import strings
import sched, time

global time_marker

# указываем токен бота
bot = telebot.TeleBot(config.token)

# get_latest_bitcoin_price получает текущий курс битка
def get_latest_bitcoin_price():
    response = requests.get(config.BITCOIN_API_URL)
    response_json = response.json()
    js = str(response.json())
    print_time("JSON = %s" % js)
    return float(response_json[0]['price_usd'])  # Конвертирует курс в число с плавающей запятой

# get_latest_eth_price получает текущий курс эфира ETH
def get_latest_eth_price():
    response = requests.get(config.ETH_API_URL)
    response_json = response.json()
    return float(response_json[0]['price_usd'])  # Конвертирует курс в число с плавающей запятой

# get_latest_eth_price получает текущий курс эфира ZCASH
def get_latest_zcash_price():
    response = requests.get(config.ZCASH_API_URL)
    response_json = response.json()
    return float(response_json[0]['price_usd'])  # Конвертирует курс в число с плавающей запятой


s = sched.scheduler(time.time, time.sleep)
def print_time(a='default'):
    print("From print_time\n", time.time(), a)


# посылаем курс биткоина пользователю в чат
def send_rate_to_user(message):
    # bot.send_message(message.chat.id, "Сегодня: %s" % str(datetime.now()))

    # отправляем пользователю сообщение с курсами 3 криптовалют
    bot.send_message(message.chat.id,
                     "BTC Price (USD) = %.4f\nETH Price (USD) = %.4f\nZCASH Price (USD) = %.4f"
                     % (get_latest_bitcoin_price(), get_latest_eth_price(), get_latest_zcash_price()))


# задача планировщику - послать пользоателю через 1 час (3600 сек) сообщение о новом курсе битка
def send_rate_delay_one_hour(message):
    s.enter(delay=60, priority=1, action=send_rate_to_user(message), argument=('positional',), kwargs={'a': 'keyword'})
    s.run()


# обработчик при старте команды - /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, strings.msg_help)

    time_marker = str(datetime.timetuple(datetime.now()))
    print ("Time_marker = %s" % time_marker)



# обработчик при старте команды - /rate - узнать курс биткоина
@bot.message_handler(commands=["rate"])
def rate(message):
    send_rate_to_user(message)


# обработчик при старте команды - /help - послать пользователю help
@bot.message_handler(commands=["help"])
def settings(message):
    bot.send_message(message.chat.id, strings.msg_help)


# самое основное тут )
if __name__ == '__main__':

# делаем так чтобы наш бот не падал когда сервер api.telegram.org выкидывает нашего бота)
    while True:
        try:
            bot.polling(none_stop=True)

        except Exception as e:
            print(str(e)) # или просто print(e) если у вас логгера нет,
            # или import traceback; traceback.print_exc() для печати полной инфы
            time.sleep(15)

        # чтобы остановить бот по нажатию CTRL-C в терминале
        except KeyboardInterrupt:
            exit()