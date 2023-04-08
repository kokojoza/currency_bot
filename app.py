import telebot
from extensions import СurrencyСonverter, APIException
import config


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(massage: telebot.types.Message):
    text = 'Бот возвращает цену на определённое количество валюты\n' \
           'Узнать доступные валюты - /values\n' \
           '<имя валюты> <в какую перевести> <количество>\n' \
           'Пример: доллар рубль 10'
    bot.reply_to(massage, text)


@bot.message_handler(commands=['values'])
def values(massage: telebot.types.Message):
    text = 'Доступные валюты: '
    for cur in config.currency.keys():
        text = '\n'.join((text, cur))
    bot.reply_to(massage, text)


@bot.message_handler(content_types=['text'])
def convert(massage: telebot.types.Message):
    try:
        value = massage.text.split(' ')
        if len(value) != 3:
            raise APIException('Много параметров! Вот пример: доллар рубль 10')

        base, quote, amount = value
        result = СurrencyСonverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(massage, f'Ошибка пользователя: {e}')
    except Exception as e:
        bot.reply_to(massage, f'Не удалось обработать команду: {e}')
    else:
        bot.reply_to(massage, result)


bot.polling(none_stop=True)
