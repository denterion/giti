from telebot import types
import telebot
import sqlite3

id_admin = 936477032
bot = telebot.TeleBot('6772021036:AAHY76lzKXiSTeiJQ9INRqER_C79LT_K7IE')

admin_panel = types.ReplyKeyboardMarkup()
admin_panel.row(types.KeyboardButton('Привелегии администартора'), types.KeyboardButton('О нашей конторе'))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте')

@bot.message_handler(commands=['admin'])
def start(message):
    if message.from_user.id == id_admin:
        bot.send_message(message.chat.id, f'Вы вошли как админ', reply_markup=admin_panel)
    else:
        bot.send_message(message.chat.id, 'Вы не администратор!')


bot.polling(non_stop=True)