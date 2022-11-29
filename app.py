import telebot
from config import currs, TOKEN
from extensions import APIException, CurrencyExchange


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message.text)
    bot.reply_to(message, f"Привет, {message.chat.username}!\n"
                          f"Чтобы увидеть список всех доступных валют, воспользуйся командой: /values.\n"
                          f"Чтобы начать конвертацию, воспользуйся командой: /exchange.")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in currs.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(commands=['exchange'])
def start_handler(message: telebot.types.Message):
    text = 'Валюта, из которой конвертировать?'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, quote_handler)


def quote_handler(message: telebot.types.Message):
    quote = message.text.strip().capitalize()
    text = 'Валюта, в которую конвертировать?'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, base_handler, quote)


def base_handler(message: telebot.types.Message, quote):
    base = message.text.strip().capitalize()
    text = 'Количество конвертируемой валюты?'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, quote, base)


def amount_handler(message: telebot.types.Message, quote, base):
    amount = message.text.strip()
    try:
        total_base = CurrencyExchange.get_price(quote, base, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации!\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
