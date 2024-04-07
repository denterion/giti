from telebot import types
import telebot
import sqlite3

id_admin = 936477031
bot = telebot.TeleBot('6772021036:AAHY76lzKXiSTeiJQ9INRqER_C79LT_K7IE')

admin_panel = types.ReplyKeyboardMarkup()
admin_panel.row(types.KeyboardButton('Привелегии администратора'), types.KeyboardButton('О нашей конторе'))

user_panel = types.ReplyKeyboardMarkup()
user_panel.row(types.KeyboardButton('Регистрация'), types.KeyboardButton('Число удачи'))


@bot.message_handler(commands=['start'])
def start_func(message):
    bot.send_message(message.chat.id, 'Здравствуйте')

@bot.message_handler(commands=['admin'])
def admin_func(message):
    if message.from_user.id == id_admin:
        bot.send_message(message.chat.id, f'Вы вошли как админ', reply_markup=admin_panel)
    else:
        bot.send_message(message.chat.id, 'Вы не администратор!')

@bot.message_handler(commands=['user'])
def user_func(message):
    if message.from_user.id != id_admin:
        bot.send_message(message.chat.id, f'Вы вошли как {message.from_user.first_name, message.from_user.last_name}', reply_markup=user_panel)

def privilege_func(message):
    bot.send_message(message.chat.id, 'Привелегии администратора,'
                        ' это блокировать(ограничивать доступ к боту, опредленным лица),'
                        ' а также смотреть статистику бота,'
                        ' и использовать специальные команды для поддержания работы бота.')

def about_us_func(message):
    bot.send_message(message.chat.id, 'Мы интузиасты, которые работают над учетом '
                     'финансового сектора РФ')

def registration_func(message):
    bot.send_message(message.chat.id, 'Введите вашу почту')
    if '@' in message.text:
        user_email = message.text
        bot.send_message(message.chat.id, 'Введите пароль')
        user_password = message.text
        bot.send_message(message.chat.id, f'Регистрация пройдена, ваши данные: {user_email, user_password}')

@bot.message_handler()
def sundry_func(message):
    if message.text == 'admin':
        admin_func(message)
    elif message.text == 'start':
        start_func(message)
    elif message.text == 'Привелегии администратора':
        privilege_func(message)
    elif message.text == 'О нашей конторе':
        about_us_func(message)
    elif message.text == 'Регистрация':
        registration_func(message)
    else:
        bot.send_message(message.chat.id, 'Используйте команды или заготовленные слова')

bot.polling(non_stop=True)