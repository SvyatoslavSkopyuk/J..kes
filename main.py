import telebot
import shelve

from random import choice
from parser import give_joke, parse

bot = telebot.TeleBot('1738958667:AAGvgXWxuzHzRPQWb8lxkf33NOtmfU0cOqA')
parse()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    :param message: сообщение, на которое надо ответить
    """
    bot.reply_to(message, f'Я бот-анекдотер, отправляю гэги на английском. '
                          f'Введи команду /categories, чтобы увидеть список различных тем. '
                          f'Если отправить мне цифру, которая стоит у каждой темы,'
                          f'я отправлю тебе рандомный анек с этой тематикой. Ломай меня, {message.from_user.first_name}. '
                          f'Ломай меня полностью.')


@bot.message_handler(commands=['categories'])
def send_categories(message):
    """
    :param message: сообщение, на которое надо ответить
    """
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
    """
    :param message: сообщение, на которое надо ответить
    """
    try:
        num = int(str(message.text).strip())
        with shelve.open('categories.db') as db:
            list_keys = list(db.keys())
            joke = choice(db[list_keys[num % len(list_keys)]])
            text = give_joke(joke)

    except ValueError:
        text = f'Введи что-то нормальное, {message.from_user.first_name}!'
    bot.send_message(
        chat_id=message.from_user.id,
        text=text,
        parse_mode="markdown"
    )


bot.polling()
