#version: 0.6.3.1
#owner: odity
import telebot
from datetime import datetime
from telebot import types,util
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
import re
import threading
import time

connection = sqlite3.connect('dmzbase.db',check_same_thread=False)
dbuser = connection.cursor()
dbuser.execute('''
CREATE TABLE IF NOT EXISTS dmzusers (
id_telegramuser TEXT PRIMARY KEY,
username TEXT,
realname TEXT,               
telephone TEXT,
status INTEGER,
datechange timestamp
)
''')

registration_stat=0
status=99
usertelegram_id=""
user_telephone=""
usertelegram_link=""
username_current=""
usernamereal_current=""
now=""
history_key=[]
history_max=8
history_file="dmzbot_history.log"
def save_history(filename,hist):
    while(True):
        time.sleep(60*5)
        print("save...")
        with open(filename, 'w') as f:
         for line in hist:
            f.write(f"{line}\n")

with open(history_file, 'r') as f:
    data = f.read()
for i in data.splitlines():
    print(i)
    history_key.append(i)
x = threading.Thread(target=save_history, args=(history_file,history_key))
x.start()

bot = telebot.TeleBot('TOKEN-KEY');
res = dbuser.execute('SELECT * FROM dmzusers WHERE id_telegramuser=?',('dmzbot',))
res = res.fetchone()

if res is None:
    dbuser.execute('INSERT INTO dmzusers (id_telegramuser, username, realname ,telephone, status,datechange) VALUES (?, ?, ?, ?, ?, ?)', ('dmzbot', '','','', 0,''))
    #dbuser.commit()
else:
    status=res[4]
    if  status == 1 or status == 2 or status == 3:
        usertelegram_id   = res[0]
        username_current  = res[1]
        usernamereal_current  = res[2]
        now=res[5]
        usernamereal_current=usernamereal_current.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
        usertelegram_link = '['+usernamereal_current+'](tg://user?id='+str(usertelegram_id)+')'
        print(usertelegram_link)
        user_telephone = res[3]
        user_telephone=user_telephone.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=")
#telebot.logger.setLevel(7)
keys = ["0","1","2","3"]
def historry_add(str):
    print(str,history_key)
    #str = str.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=")
    if len(history_key) >= history_max:
        #history_key = history_key[history_max:]
        history_key.pop(0)
    history_key.append(str)
def register_markup_finish():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("Да"),KeyboardButton("Нет"))
    return markup  
def keyboard():
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True )
    row = [KeyboardButton(x) for x in keys[:10]]
    markup.add(*row)
    markup.add(KeyboardButton("/help"),KeyboardButton("status"),KeyboardButton("history"), KeyboardButton("close keyboard"))
    return markup
   

def callback_register_data(message):
    global usernamereal_current
    usernamereal_current = message.text
    name_regex = re.compile(r'[А-яЁёa-zA-Z]+')
    t_name=""
    for item in name_regex.findall(usernamereal_current):
        t_name +=  item +" "
    usernamereal_current = t_name
    print(usernamereal_current)
   # name_regex = re.compile(r'[А-яЁёa-zA-Z]+)
    #if name_regex.findall(usernamereal_current)[0] is None:

   # print(name_regex.findall(usernamereal_current)[0])

    msg = bot.send_message(message.chat.id, 'Уважаемый '+usernamereal_current+', введите Ваш номер телефона, по которому вам могут позвонить коллеги')
    bot.register_next_step_handler(msg, callback_register_data_phone)

def callback_register_data_phone(message):
    global user_telephone
    user_telephone = message.text
    phone_regex = "([0-9]{7,14})"
    #phone_regex = re.compile(r"7\d{:10}")
    item = re.match(phone_regex, user_telephone)
    if item:
        user_telephone = item.group(0)
    else:
       # print(user_telephone)
        markup = telebot.types.ReplyKeyboardRemove()
        msg = bot.send_message(message.chat.id, "Cерьезно? Телефон должен иметь формат 7XXXxxxXXxx. Введите Ваше ФИО",
                               reply_markup=markup)  # , reply_markup=keyboardreg())
        bot.register_next_step_handler(msg, callback_register_data)
        return
    #user_telephone = phone_regex.findall(user_telephone)
    print(user_telephone)

    if user_telephone[0] == "8":
        user_telephone = '7' + user_telephone[1:]
    if user_telephone[0] != "+":
        user_telephone = '+' + user_telephone[0:]

    msg = bot.send_message(message.chat.id, 'Ваш номер: '+user_telephone+'. Все верно?', reply_markup=register_markup_finish())

#Надо редактировать  
@bot.my_chat_member_handler()
def my_chat_m(message: types.ChatMemberUpdated):
    old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member":
        bot.send_message(message.chat.id,"Кто хочет узнать статус ключа - поднимите руку :)") # Welcome message, if bot was added to group
        bot.leave_chat(message.chat.id)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    #print(usertelegram_id)
    bot.send_message(message.from_user.id, """\
0-Ключ на ресепшене, ДЗ на охране
1-Ключ на ресепшене, ДЗ не на охране. Установил %username% c %phone% в %date%
2-ДЗ закрыт на ключ, ключ у %username_current% c %date% (contact: +7...) 
3-ДЗ открыт, ключ у %username_current%  c %date% (contact: +7...)
/register - изменить свое имя и номер телефона
history - история статуса ключа
status- показать статус
+74957300945 - телефон для снятия с охраны демозала
    """,reply_markup=keyboard())

@bot.message_handler(func=lambda message: True, content_types=['text'])
#@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global dbuser
    global status
    global usertelegram_id
    global user_telephone
    global usertelegram_link
    global username_current
    global usernamereal_current
    global registration_stat
    global now
    if registration_stat == 1 and message.text == "Нет":
        markup = telebot.types.ReplyKeyboardRemove()
        msg=bot.send_message(message.chat.id, "Введите Ваше ФИО",reply_markup=markup)#, reply_markup=keyboardreg())
        bot.register_next_step_handler(msg, callback_register_data)
        return
    if registration_stat == 1 and message.text == "Да":
        registration_stat = 0

        get = dbuser.execute('SELECT * FROM dmzusers WHERE id_telegramuser=?',(message.from_user.id,))
        get = get.fetchone()
        if get is not None:
            dbuser.execute('UPDATE dmzusers SET realname=?,telephone=? WHERE id_telegramuser=?', (usernamereal_current, user_telephone, message.from_user.id))       
        else:
            dbuser.execute('INSERT INTO dmzusers (id_telegramuser,username, realname, telephone) VALUES (?, ?, ?, ?)', (message.from_user.id,message.from_user.first_name , usernamereal_current, user_telephone))
        connection.commit() 
        bot.send_message(message.from_user.id, "Регистрация прошла успешно",reply_markup=keyboard())
        return


    res = dbuser.execute('SELECT COUNT(id_telegramuser) FROM dmzusers WHERE id_telegramuser = ?',(message.from_user.id,))
    if  res.fetchone()[0] == 0 or message.text == "/register":
        registration_stat = 1
        markup = telebot.types.ReplyKeyboardRemove()
        msg=bot.send_message(message.chat.id, "Зарегистрироваться надо бы. Введите Ваше ФИО",reply_markup=markup)#, reply_markup=keyboardreg())
        bot.register_next_step_handler(msg, callback_register_data)
        return
    #bot.send_message(message.chat.id, "Мне нужно узнать ваш номер телефон,чтобы другие могли бы вам позвонить", reply_markup=keycontact())
    if message.text == "close keyboard":
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id,"Клавиатуру закрыл",reply_markup=markup)
    elif message.text == "/start" or message.text == "/help":
        bot.register_next_step_handler(message.text, send_welcome(message.text))
    elif message.text == "history":
        history_string=''
        if len(history_key) <1:
            return
        for item in history_key:
            history_string=history_string+"\n"+item
        bot.send_message(message.chat.id, f"{history_string}")

    elif message.text == "status":
        res = dbuser.execute('SELECT * FROM dmzusers WHERE id_telegramuser=?',('dmzbot',))
        res = res.fetchone()
        status=res[4]
        now=res[5]
        user_telephone=res[3]
        user_telephone=user_telephone.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
        usertelegram_id=res[2]
        usertelegram_id=usertelegram_id.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
        if status == 0:
            tmp_str=str(f"Статус: Ключ на ресепшене, ДЗ на охране")
            bot.send_message(message.chat.id, tmp_str)
        if status == 1:
            print(usertelegram_link)
            tmp_str=str(f"Статус: Ключ на ресепшене, ДЗ не на охране\\. Инициатор: {usertelegram_link} по телефону: {user_telephone} отдал ключ в *{now}*")
            bot.send_message(message.chat.id, f"{tmp_str}",parse_mode='MarkdownV2',disable_web_page_preview=True)
            print("2")
            #bot.send_message(message.chat.id, f'Его номер телефон: {user_telephone}')
        if status == 2:
            tmp_str=str(f"Статус: ДЗ закрыт на ключ, ключ у {usertelegram_link} ")
            bot.send_message(message.chat.id, f'{tmp_str} c *{now}*\\. Его телефон: {user_telephone}',parse_mode='MarkdownV2',disable_web_page_preview=True)
            #bot.send_message(message.chat.id, f'Его номер телефон: {user_telephone}')
        if status == 3:
            tmp_str=str(f"Статус: ДЗ открыт, ключ у {usertelegram_link} ")
            bot.send_message(message.chat.id,f'{tmp_str} c *{now}*\\. Его телефон: {user_telephone}',parse_mode='MarkdownV2',disable_web_page_preview=True)
            #bot.send_message(message.chat.id, f'Его номер телефон: {user_telephone}')
    elif message.text == "0":
        msg = bot.reply_to(message, "Статус: Ключ на ресепшене, ДЗ на охране")
        status=0
        get = dbuser.execute('SELECT * FROM dmzusers WHERE id_telegramuser=?',(message.from_user.id,))
        get = get.fetchone()
        if get is not None:
            user_telephone = get[3]
           # user_telephone = user_telephone.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace( "+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
            usertelegram_link = '[' + usertelegram_id + '](tg://user?id=' + str(message.from_user.id) + ')'
            usertelegram_id = get[2]
            usertelegram_id = usertelegram_id.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`","\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
            #usertelegram_link = '[' + usertelegram_id + '](tg://user?id=' + str(message.from_user.id) + ')'

            dbuser.execute('UPDATE dmzusers SET username=?,realname=?,telephone=?,status=? WHERE id_telegramuser="dmzbot"', (message.from_user.first_name,get[2],get[3] , status))
        else:
            usertelegram_id = message.from_user.first_name
            usertelegram_id = usertelegram_id.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`","\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
           # usertelegram_link = '[' + usertelegram_id + '](tg://user?id=' + str(message.from_user.id) + ')'

            dbuser.execute('UPDATE dmzusers SET username=?,status=? WHERE id_telegramuser="dmzbot"', (message.from_user.first_name , status))
        connection.commit()

        #now = datetime.now()
        #now = now.strftime("%H:%M:%S %d/%m/%Y")
        #usertelegram_id=message.from_user.first_name

        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
       # historry_add(f"{now}: Ключ на ресепшене, ДЗ на охране. Установил {usertelegram_id} ")
        historry_add(f"{now}: Ключ на ресепшене, ДЗ на охране. Установил {usertelegram_id} по телефону: {user_telephone}")

    elif message.text == "1":
        msg = bot.reply_to(message, "Статус: Ключ на ресепшене, ДЗ не на охране")
        status=1
        now = datetime.now()
        now = now.strftime("%H:%M:%S %d/%m/%Y")
        print(now)
        get = dbuser.execute('SELECT * FROM dmzusers WHERE id_telegramuser=?',(message.from_user.id,))
        get = get.fetchone()
        if get is not None:
            usertelegram_id=get[2]
            usertelegram_id=usertelegram_id.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
            user_telephone = get[3]
            user_telephone=user_telephone.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
            usertelegram_link = '['+usertelegram_id+'](tg://user?id='+str(message.from_user.id)+')'
            dbuser.execute('UPDATE dmzusers SET username=?,realname=?,telephone=?,status=?,datechange=? WHERE id_telegramuser="dmzbot"', (message.from_user.first_name,get[2],get[3] , status, now))
        else:
            usertelegram_id=message.from_user.first_name
            dbuser.execute('UPDATE dmzusers SET username=?,status=?,datechange=? WHERE id_telegramuser="dmzbot"', (message.from_user.first_name , status,now))
        connection.commit()
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
        user_telephone = get[3]
        historry_add(f"{now}: Ключ на ресепшене, ДЗ не на охране. Установил {usertelegram_id} по телефону: {user_telephone}")
    elif message.text == "2":
        status=2
        get = dbuser.execute('SELECT * FROM dmzusers WHERE id_telegramuser=?',(message.from_user.id,))
        get = get.fetchone()
        now = datetime.now()
        now = now.strftime("%H:%M:%S %d/%m/%Y")
        print(now)
        if get is not None:
            usertelegram_id=get[2]
            usertelegram_id=usertelegram_id.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
            usertelegram_link = '['+usertelegram_id+'](tg://user?id='+str(message.from_user.id)+')'
        else:
            usertelegram_id=message.from_user.first_name
            usertelegram_id=usertelegram_id.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
            usertelegram_link = '['+usertelegram_id+'](tg://user?id='+str(message.from_user.id)+')'
        tmp_str=str(f"Статус: ДЗ закрыт на ключ, ключ у {usertelegram_link}")
        bot.send_message(message.chat.id, f'{tmp_str}',parse_mode='MarkdownV2',disable_web_page_preview=True)
        
        if get is not None:
            dbuser.execute('UPDATE dmzusers SET username=?,realname=?,telephone=?,status=?,datechange=? WHERE id_telegramuser="dmzbot"', (message.from_user.first_name,get[2],get[3] , status,now))
        else:
            dbuser.execute('UPDATE dmzusers SET username=?,status=?,datechange=? WHERE id_telegramuser="dmzbot"', (message.from_user.first_name , status,now))
        connection.commit()

        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
        user_telephone = get[3]
        historry_add(f"{now}: ДЗ закрыт на ключ, ключ у {usertelegram_id}.  Установил {usertelegram_id} по телефону: {user_telephone}")
    elif message.text == "3":
        status=3
        get = dbuser.execute('SELECT * FROM dmzusers WHERE id_telegramuser=?',(message.from_user.id,))
        get = get.fetchone()
        now = datetime.now()
        now = now.strftime("%H:%M:%S %d/%m/%Y")
        print(now)
        if get is not None:
            usertelegram_id=get[2]
            usertelegram_id=usertelegram_id.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
            usertelegram_link = '['+usertelegram_id+'](tg://user?id='+str(message.from_user.id)+')'
        else:
            usertelegram_id=message.from_user.first_name
            usertelegram_id=usertelegram_id.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace("-", "\\-").replace(".", "\\.").replace(",", "\\,").replace("=", "\\=");
            usertelegram_link = '['+usertelegram_id+'](tg://user?id='+str(message.from_user.id)+')'
        tmp_str=str(f"Статус: ДЗ открыт, ключ у {usertelegram_link}")
        bot.send_message(message.chat.id, f'{tmp_str}',parse_mode='MarkdownV2',disable_web_page_preview=True)
        get = dbuser.execute('SELECT * FROM dmzusers WHERE id_telegramuser=?',(message.from_user.id,))
        get = get.fetchone()
        if get is not None:
            dbuser.execute('UPDATE dmzusers SET username=?,realname=?,telephone=?,status=?,datechange=? WHERE id_telegramuser="dmzbot"', (message.from_user.first_name,get[2],get[3] , status,now))
        else:
            dbuser.execute('UPDATE dmzusers SET username=?,status=?,datechange=? WHERE id_telegramuser="dmzbot"', (message.from_user.first_name , status,now))
        connection.commit()
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
        user_telephone = get[3]
        historry_add(f"{now}: ДЗ открыт, ключ у {usertelegram_id}.  Установил {usertelegram_id} по телефону: {user_telephone}")

    else:
        msg = bot.reply_to(message, "Неверный статус")
    print(f"id={message.from_user.id} user={message.from_user.first_name} status={status}: {message.text}")
    usertelegram_id=message.from_user.first_name
    #print (message.contact.phone_number) 

        
#bot.polling(none_stop=True, interval=0)
bot.infinity_polling(timeout=10, long_polling_timeout = 5)
connection.commit()
connection.close()
