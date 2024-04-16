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
    bot.send_message(message.chat.id, 'Чтобы войти как админ используйте команду /admin')
    bot.send_message(message.chat.id, 'Чтобы войти как пользователь используйте команду /user')


'''Функция user'''
@bot.message_handler(commands=['user'])
def user_func(message):
    user_panel = types.ReplyKeyboardMarkup()
    user_panel.row(types.KeyboardButton('Регистрация'), types.KeyboardButton('Вернуться в начало'), types.KeyboardButton('Войти'),
                   types.KeyboardButton('План питания'))
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

"""План питания"""
@bot.message_handler(commands=['meal_plan'])
def meal_plan_func(message):
    markup_plan_meal = types.ReplyKeyboardMarkup()
    markup_plan_meal.row(types.KeyboardButton('1-day'), types.KeyboardButton('2-day'),
                         types.KeyboardButton('3-day'), types.KeyboardButton('4-day'),
                         types.KeyboardButton('5-day'), types.KeyboardButton('6-day'),
                         types.KeyboardButton('7-day'))
    markup_plan_meal.add(types.KeyboardButton('Вернуться в начало'))
    bot.send_message(message.chat.id, 'Сейчас мы составим план питания вам на неделю', reply_markup=markup_plan_meal)

'''Первый день плана питания'''
def day_plan_1(message):
    markup_1_day = types.ReplyKeyboardMarkup()
    markup_1_day.row(types.KeyboardButton('План питания'), types.KeyboardButton('Вернуться в начало'))
    bot.send_message(message.chat.id, 'План 1 дня', reply_markup=markup_1_day)
    bot.send_document(message.chat.id, open("План_Питания/1-день.txt", "rb"))

def day_plan_2(message):
    markup_1_day = types.ReplyKeyboardMarkup()
    markup_1_day.row(types.KeyboardButton('План питания'), types.KeyboardButton('Вернуться в начало'))
    bot.send_message(message.chat.id, 'План 2 дня', reply_markup=markup_1_day)
    bot.send_document(message.chat.id, open("План_Питания/2-день.txt", "rb"))

def day_plan_3(message):
    markup_1_day = types.ReplyKeyboardMarkup()
    markup_1_day.row(types.KeyboardButton('План питания'), types.KeyboardButton('Вернуться в начало'))
    bot.send_message(message.chat.id, 'План 3 дня', reply_markup=markup_1_day)
    bot.send_document(message.chat.id, open("План_Питания/3-день.txt", "rb"))

def day_plan_4(message):
    markup_1_day = types.ReplyKeyboardMarkup()
    markup_1_day.row( types.KeyboardButton('План питания'), types.KeyboardButton('Вернуться в начало'))
    bot.send_message(message.chat.id, 'План 4 дня', reply_markup=markup_1_day)
    bot.send_document(message.chat.id, open("План_Питания/4-день.txt", "rb"))

def day_plan_5(message):
    markup_1_day = types.ReplyKeyboardMarkup()
    markup_1_day.row(types.KeyboardButton('План питания'), types.KeyboardButton('Вернуться в начало'))
    bot.send_message(message.chat.id, 'План 5 дня', reply_markup=markup_1_day)
    bot.send_document(message.chat.id, open("План_Питания/5-день.txt", "rb"))

def day_plan_6(message):
    markup_1_day = types.ReplyKeyboardMarkup()
    markup_1_day.row(types.KeyboardButton('План питания'), types.KeyboardButton('Вернуться в начало'))
    bot.send_message(message.chat.id, 'План 6 дня', reply_markup=markup_1_day)
    bot.send_document(message.chat.id, open("План_Питания/6-день.txt", "rb"))

def day_plan_7(message):
    markup_1_day = types.ReplyKeyboardMarkup()
    markup_1_day.row(types.KeyboardButton('План питания'), types.KeyboardButton('Вернуться в начало'))
    bot.send_message(message.chat.id, 'План 7 дня', reply_markup=markup_1_day)
    bot.send_document(message.chat.id, open("План_Питания/7-день.txt", "rb"))


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
    markup_1_day_back.row(types.KeyboardButton('Вернуться в начало'), types.KeyboardButton('План питания'))
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
    elif message.text == '1-day':
        day_plan_1(message)
    elif message.text == '2-day':
        day_plan_2(message)
    elif message.text == '3-day':
        day_plan_3(message)
    elif message.text == '4-day':
        day_plan_4(message)
    elif message.text == '5-day':
        day_plan_5(message)
    elif message.text == '6-day':
        day_plan_6(message)
    elif message.text == '7-day':
        day_plan_7(message)
    elif message.text == 'Войти':
        login_func(message)
    elif message.text == 'Вы успешно зашли':
        pass
    else:
        bot.reply_to(message, 'Это точно команда или кодовое слово? Или Вы не админ?')
        logging.info('Ответ отправлен')


bot.polling(non_stop=True)
