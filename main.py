from telebot import types
import telebot
import sqlite3
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)
id_admin = 936477032
bot = telebot.TeleBot('6772021036:AAHY76lzKXiSTeiJQ9INRqER_C79LT_K7IE')

'''Функция старт'''
@bot.message_handler(commands=['start'])
def start_func(message):
    start_panel = types.ReplyKeyboardMarkup()
    start_panel.row(types.KeyboardButton('/admin'), types.KeyboardButton('/user'))
    bot.send_message(message.chat.id, 'Здравстуйте, это телеграм бот под названием zOL(Здоровый Образ жизни)')
    bot.send_message(message.chat.id, 'Вы хотите войти как пользователь или как админ?', reply_markup=start_panel)
    bot.send_message(message.chat.id, 'Чтобы войти как админ используйте команду "/admin"')
    bot.send_message(message.chat.id, 'Чтобы войти как пользователь используйте команду "/user"')

'''Функция user'''
@bot.message_handler(commands=['user'])
def user_func(message):
    user_panel = types.ReplyKeyboardMarkup()
    user_panel.row(types.KeyboardButton('Регистрация'), types.KeyboardButton('Вернуться в начало'))
    bot.send_message(message.chat.id, 'Здравствуйте дорогой пользователь, команды специально для вас', reply_markup=user_panel)


'''Функция админ'''
@bot.message_handler(commands=['admin'])
def admin_func(message):
    back_to_start = types.ReplyKeyboardMarkup()
    back_to_start.add(types.KeyboardButton('Вернуться в начало'))
    if message.from_user.id != id_admin:
        bot.send_message(message.chat.id, 'Вы не админ!', reply_markup=back_to_start)
    if message.from_user.id == id_admin:
        markup_admin = types.ReplyKeyboardMarkup()
        markup_admin.row(types.KeyboardButton('Посмотреть список пользователей'), types.KeyboardButton('Вернуться в начало'))
        bot.send_message(message.chat.id, 'Команды админа', reply_markup=markup_admin)


'''Регистрация usera'''
@bot.message_handler(commands=['registration'])
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
    markup_back = types.ReplyKeyboardMarkup()
    markup_back.add(types.KeyboardButton('Вернуться в начало'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрован', reply_markup=markup_back)


'''Функция получения всех пользователей для админа'''
@bot.message_handler(commands=['array'])
def array_func(message):
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


'''Обработчик сообщений'''
@bot.message_handler()
def sundry_func(message):
    if message.text == 'Посмотреть список пользователей' and message.from_user.id == id_admin:
        array_func(message)
    elif message.text == 'Вернуться в начало':
        start_func(message)
    elif message.text == 'admin' and message.from_user.id == id_admin:
        admin_func(message)
    elif message.text == 'Регистрация':
        reg_func(message)
    else:
        bot.reply_to(message, 'Это точно команда или кодовое слово? Или Вы не админ?')
        logging.info('Ответ отправлен')


bot.polling(non_stop=True)
