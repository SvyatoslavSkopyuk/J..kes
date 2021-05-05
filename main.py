import telebot
import shelve

from random import choice
from parser import give_joke, parse
bot = telebot.TeleBot('1738958667:AAGvgXWxuzHzRPQWb8lxkf33NOtmfU0cOqA')
parse()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот-telebot. А ты чмо, {message.from_user.first_name}')


@bot.message_handler(commands=['categories'])
def send_categories(message):
    with shelve.open('categories.db') as db:
        list_keys = list(db.keys())
        text = ''
        for i in range(len(list_keys)):
            text += str(i) + "." + list_keys[i].replace("-", " ").title() + "\n"
    bot.send_message(
        chat_id=message.from_user.id,
        text=text
    )

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    try:
        num = int(str(message.text).strip())
        with shelve.open('categories.db') as db:
            list_keys = list(db.keys())
            joke = choice(db[list_keys[num % len(list_keys)]])
            text = give_joke(joke)

    except ValueError:
        text = 'Введи что-то нормальное, Макар, сука!'
    bot.send_message(
        chat_id=message.from_user.id,
        text=text,
        parse_mode="markdown"
    )



bot.polling()
