import telebot
from config import currs, TOKEN
from extensions import APIException, CurrencyExchange


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message.text)
    bot.reply_to(message, f"Привет, {message.chat.username}! Введи свой запрос в формате:\n"
                          f" <имя валюты, цену которой хочешь узнать> "
                          f"<имя валюты, в которой надо узнать цену первой валюты> "
                          f"<количество первой валюты>. \n"
                          f"Чтобы увидеть список всех доступных валют, воспользуйся командой: /values.")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in currs.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def exchange(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        quote, base, amount = values
        total_base = CurrencyExchange.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
