
import telebot
from telebot import types

# 1667430363:AAE3xah4t2Y_sg4ydYb5XCDyqcqZACTysrI
# GIT guide https://www.youtube.com/watch?v=9VKKZNqzPcE

name = ''
surname = ''
age = 0

bot = telebot.TeleBot("1667430363:AAE3xah4t2Y_sg4ydYb5XCDyqcqZACTysrI",
                      parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Вижу у нас новый посетитель, ну поехали :)")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == 'Привет':
        #bot.reply_to(message, 'Приветики :)')
        #elif message.text == 'привет':
        #bot.reply_to(message, 'Приветик :)')
        #elif message.text == '/reg':
        bot.send_message(message.from_user.id, "Привет! Давай познакомимся! Как тебя зовут? :)")
        bot.register_next_step_handler(message, reg_name)
    # bot.reply_to(message, message.text)

def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Отлично! Скажи еще свою фамилию, пожалуйста :)")
    bot.register_next_step_handler(message, reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "А сколько тебе лет?")
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Ой, что-то не так... тебе нужно вводить возраст цифрами.")
            break
    if age == 0:
        bot.register_next_step_handler(message, reg_age)
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='да', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='нет', callback_data='no')
        keyboard.add(key_no)
        question = 'Тебе ' + str(age) + ' ? и тебя зовут: ' + name + ' ' + surname + '?'
        bot.send_message(message.from_user.id, text = question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global name
    global surname
    global age
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Приятно познакомиться!")
    elif call.data == "no":
        name = ''
        surname = ''
        age = 0
        bot.send_message(call.message.chat.id, "Попробуем еще раз!")
        bot.send_message(call.message.chat.id, "Привет! Давай познакомимся! Как тебя зовут?")
        bot.register_next_step_handler(call.message, reg_name)

bot.polling()
