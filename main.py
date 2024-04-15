from telebot import types
import telebot
import sqlite3
import logging
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)
id_admin = 936477032 #айди админа
bot = telebot.TeleBot('6772021036:AAHY76lzKXiSTeiJQ9INRqER_C79LT_K7IE') #токен ботика


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
    user_panel.row(types.KeyboardButton('Регистрация'), types.KeyboardButton('Вернуться в начало'), types.KeyboardButton('Войти'))
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


@bot.message_handler(commands=['meal_plan'])
def meal_plan_func(message):
    markup_plan_meal = types.ReplyKeyboardMarkup()
    markup_plan_meal.row(types.KeyboardButton('1_day_meal'), types.KeyboardButton('2_day_meal'),
                         types.KeyboardButton('3_day_meal'), types.KeyboardButton('4_day_meal'),
                         types.KeyboardButton('5_day_meal'), types.KeyboardButton('6_day_meal'),
                         types.KeyboardButton('7_day_meal'))
    bot.send_message(message.chat.id, 'Сейчас мы составим план питания на неделю', reply_markup=markup_plan_meal)
    bot.register_next_step_handler(message, day_plan_1)


def day_plan_1(message):
    markup_1_day = types.ReplyKeyboardMarkup()
    markup_1_day.row(types.KeyboardButton('Завтрак1'), types.KeyboardButton('Обед1'),
                     types.KeyboardButton('Ужин1'), types.KeyboardButton('Перекус1'))
    bot.send_message(message.chat.id, 'Каждый день состоит из 3 приемов пищи и одного перекуса', reply_markup=markup_1_day)


'''Функция для получения имя пользователя из бд'''
@bot.message_handler(commands=['login'])
def login_func(message):
    bot.send_message(message.chat.id, 'Введите имя пользователя, которое вы указали при регистрации')
    bot.register_next_step_handler(message, login_name_func)


'''Получение имя пользователя для входа'''
def login_name_func(message):
    global user_name_from_bd
    user_name_from_bd = message.text.strip()
    with open('users.json') as f:
        file_content = f.read()
        templates = json.loads(file_content)
    markup_login = types.ReplyKeyboardMarkup()
    markup_login.add(types.KeyboardButton('Вернуться в начало'))
    for name in templates.values():
        for i in name:
            if i == user_name_from_bd:
                bot.send_message(message.chat.id, 'Введите пароль')
                bot.register_next_step_handler(message, login_password_func)
                break
    else:
        bot.send_message(message.chat.id, 'Повторите попытку снова', reply_markup=markup_login)


'''Получение пароля для входа'''
def login_password_func(message):
    global password_login
    password_login = message.text.strip()
    with open('users.json') as f:
        file_content = f.read()
        templates = json.loads(file_content)
    markup_login = types.ReplyKeyboardMarkup()
    markup_login.add(types.KeyboardButton('Вернуться в начало'))
    for i in templates.values():
        for j in range(len(i)):
            if i[j] == password_login:
                bot.send_message(message.chat.id, 'Вы успешно зашли', reply_markup=markup_login)
                break
    else:
        bot.send_message(message.chat.id, 'Повторите попытку снова', reply_markup=markup_login)
                


'''получение имя пользователя'''
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль!')
    bot.register_next_step_handler(message, user_password)


'''получение пароля пользователя'''
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
    name = []
    passwords = []
    for i in users:
        if i[1] not in name:
            name.append(i[1])
        if i[2] not in passwords:
            passwords.append(i[2])
    
    to_json = {'Name_users': name, 'Passwords_users': passwords}
    
    with open('users.json', 'w') as f:
        f.write(json.dumps(to_json))
    
    with open('users.json') as f:
        bot.send_message(message.chat.id, 'Список пользователей')
        bot.send_message(message.chat.id, f.read())
    cursor.close()
    connection.close()


'''Обработчик сообщений'''
@bot.message_handler()
def sundry_func(message):
    markup_1_day_back = types.ReplyKeyboardMarkup()
    markup_1_day_back.row(types.KeyboardButton('Вернуться в начало'), types.KeyboardButton('План питания'),
                          types.KeyboardButton('Завтрак1'), types.KeyboardButton('Обед1'),
                          types.KeyboardButton('Ужин1'), types.KeyboardButton('Перекус1'))
    if message.text == 'Посмотреть список пользователей' and message.from_user.id == id_admin:
        array_func(message)
    elif message.text == 'Вернуться в начало':
        start_func(message)
    elif message.text == 'admin' and message.from_user.id == id_admin:
        admin_func(message)
    elif message.text == 'План питания':
        meal_plan_func(message)
    elif message.text == 'Регистрация':
        reg_func(message)
    elif message.text == '1_day_meal':
        bot.register_next_step_handler(message, day_plan_1)
    elif message.text == 'Войти':
        login_func(message)
    elif message.text == 'Вы успешно зашли':
        pass
    elif message.text == 'Завтрак1':
        bot.reply_to(message, 'Завтрак: Омлет из двух яиц с овощами и зеленью.', reply_markup=markup_1_day_back)
    elif message.text == 'Обед1':
        bot.reply_to(message, 'Обед: Греческий салат с куриной грудкой.', reply_markup=markup_1_day_back)
    elif message.text == 'Ужин1':
        bot.reply_to(message, 'Ужин: Запеченый лосось с овощами.', reply_markup=markup_1_day_back)
    elif message.text == 'Перекус1':
        bot.reply_to(message, 'Перекус: Грейпфрут.', reply_markup=markup_1_day_back)
    else:
        bot.reply_to(message, 'Это точно команда или кодовое слово? Или Вы не админ?')
        logging.info('Ответ отправлен')


bot.polling(non_stop=True)
