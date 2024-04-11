from telebot import types
import telebot
import sqlite3
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

id_admin = 936477032
bot = telebot.TeleBot('6772021036:AAHY76lzKXiSTeiJQ9INRqER_C79LT_K7IE')

admin_panel = types.ReplyKeyboardMarkup()
admin_panel.row(types.KeyboardButton('Привелегии администратора'), types.KeyboardButton('О нашей конторе'))

@bot.message_handler(commands=['start'])
def start_func(message):
    bot.send_message(message.chat.id, 'Здравстуйте, это телеграм бот под названием zOL(Здоровый Образ жизни)')
    bot.send_message(message.chat.id, 'Вы хотите войти как пользователь или как админ?')
    bot.send_message(message.chat.id, 'Чтобы войти как админ используйте команду "/admin"')
    bot.send_message(message.chat.id, 'Чтобы войти как пользователь используйте команду "/user"')

@bot.message_handler(commands=['reg'])
def reg_func(message):
    connection = sqlite3.connect('telebot.sql')
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id integer auto_increment primary key, name varchar(50), password varchar(50))')
    connection.commit()
    cursor.close()
    connection.close()

    bot.send_message(message.chat.id, 'Введите ваше имя пользователя!')
    bot.register_next_step_handler(message, user_name)
    logging.info('Команда регистрация запущена')


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль!')
    bot.register_next_step_handler(message, user_password)

def user_password(message):
    password = message.text.strip()
    connection = sqlite3.connect('telebot.sql')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (name, password) VALUES ('%s', '%s')" % (name, password))
    connection.commit()
    cursor.close()
    connection.close()
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('Посмотреть список пользователей'), types.KeyboardButton('Вернуться в самое начало'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрован', reply_markup=markup)

@bot.message_handler(commands=['admin'])
def admin_func(message):
    connection = sqlite3.connect('telebot.sql')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    info = ''
    for i in users:
        info += f'Имя: {i[1]}, Пароль: {i[2]}\n'
    cursor.close()
    connection.close()
    bot.send_message(message.chat.id, 'Список пользователей')
    bot.send_message(message.chat.id, info)

@bot.message_handler()
def sundry_func(message):
    if message.text == 'Посмотреть список пользователей' and message.from_user.id == id_admin:
        admin_func(message)
    elif message.text == 'Вернуться в самое начало':
        start_func(message)
    else:
        bot.reply_to(message, 'Это точно команда или кодовое слово? Или Вы не админ?')
        logging.info('Ответ отправлен')

bot.polling(non_stop=True)
