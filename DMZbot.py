#version 0.4.1 by odity
import telebot
from telebot import types,util

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
status=99
status_id="None"
status_user="None"
user_key=""
bot = telebot.TeleBot('TOKEN');
#telebot.logger.setLevel(7)
keys = ["0","1","2","3","4","5","6","/help"]

def keyboard():
    markup = ReplyKeyboardMarkup(row_width=4)
    row = [KeyboardButton(x) for x in keys[:10]]
    markup.add(*row)
    markup.add(KeyboardButton("status"))
    markup.add(KeyboardButton("close keyboard"))

    return markup
@bot.my_chat_member_handler()
def my_chat_m(message: types.ChatMemberUpdated):
    old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member":
        bot.send_message(message.chat.id,"Кто хочет узнать статус ключа - поднимите руку :)") # Welcome message, if bot was added to group
     #   bot.leave_chat(message.chat.id)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    #bot.send_message(message.from_user.id,"",reply_markup=keyboard())
    bot.send_message(message.from_user.id, """\
0-Ключ на ресепшене
1-Ключ у %username% в офисе
2-Ключ у %username% в ДЗ
3-ДЗ закрыт на ключ и СКУД
4-ДЗ закрыт на ключ, без СКУД
5-ДЗ открыт
6-Передал ключ %username%
status- показать статус
    """,reply_markup=keyboard())

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global status
    global status_id
    global status_user
    global user_key
    #status_id=message.from_user.first_name
    #linked_user = '[@'+status_id+'](tg://user?id='+str(message.from_user.id)+')'    
    #f'{linked_user}'
    #print(f"id={message.from_user.id} user={message.from_user.first_name} status={status}")
    if message.text == "close keyboard":
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id,"Клавиатуру закрыл",reply_markup=markup)
    elif message.text == "/start" or message.text == "/help":
        bot.register_next_step_handler(message.text, send_welcome(message.text))
    elif message.text == "status":
        if status == 0:
            tmp_str=str(f"Ключ на ресепшене")
            bot.send_message(message.chat.id, tmp_str)
        if status == 1:
            tmp_str=str(f"Ключ у {status_user} в офисе")
            bot.send_message(message.chat.id, f'{tmp_str}',parse_mode='MarkdownV2',disable_web_page_preview=True)
        if status == 2:
            tmp_str=str(f"Ключ у {status_user} в ДЗ")
            bot.send_message(message.chat.id, f'{tmp_str}',parse_mode='MarkdownV2',disable_web_page_preview=True)
            #bot.send_message(message.chat.id, tmp_str)
        if status == 3:
            tmp_str=str(f"ДЗ закрыт на ключ и СКУД")
            bot.send_message(message.chat.id, tmp_str)
        if status == 4:
            tmp_str=str(f"ДЗ закрыт на ключ, без СКУД")
            bot.send_message(message.chat.id, tmp_str)
        if status == 5:
            tmp_str=str(f"ДЗ открыт")
            bot.send_message(message.chat.id, tmp_str)
        if status == 6:
            tmp_str=str(f"Ключ передал {user_key}")
            bot.send_message(message.chat.id, tmp_str)
        if status == 99:
            tmp_str=str(f"Ooops...Reset status")
            bot.send_message(message.chat.id, tmp_str)
    elif message.text == "0":
        msg = bot.reply_to(message, "Ключ на ресепшене")
        status=0
        status_id=message.from_user.first_name
        linked_user = '[@'+status_id+'](tg://user?id='+str(message.from_user.id)+')'
        #bot.reply_to(message, status)
        user_key=""
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "1":
        msg = bot.reply_to(message, "Ключ у меня в офисе")
        status_id=message.from_user.first_name
        status_user = '[@'+status_id+'](tg://user?id='+str(message.from_user.id)+')'
        status=1
        user_key=""
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "2":
        msg = bot.reply_to(message, "Ключ у меня в ДЗ")
        status_id=message.from_user.first_name
        status_user = '[@'+status_id+'](tg://user?id='+str(message.from_user.id)+')'
        status=2
        user_key=""
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "3":
        msg = bot.reply_to(message, "ДЗ закрыт на ключ и СКУД")
        status_id=message.from_user.first_name
        status_user = '[@'+status_id+'](tg://user?id='+str(message.from_user.id)+')'
        status=3
        user_key=""
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "4":
        msg = bot.reply_to(message, "ДЗ закрыт на ключ, без СКУД")
        status_id=message.from_user.first_name
        status_user = '[@'+status_id+'](tg://user?id='+str(message.from_user.id)+')'
        status=4
        user_key=""
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "5":
        msg = bot.reply_to(message, "ДЗ открыт")
        status_id=message.from_user.first_name
        status_user = '[@'+status_id+'](tg://user?id='+str(message.from_user.id)+')'
        status=5
        #bot.register_next_step_handler(msg, show_status)
        #msg = bot.reply_to(message, status)
        user_key=""
    elif message.text == "6":
        status=6
      #  bot.send_message(message.chat.id, 'Кому вы передали ключ?')
        bot.register_next_step_handler(message, enter_user)
        #msg = bot.reply_to(message, "Ключ передал "+str(user_key))

   #     status_id=message.from_user.first_name
   #     status_user = '[@'+status_id+'](tg://user?id='+str(message.from_user.id)+')'
        #
    elif message.text == "DMZchat_id":
        print(message.chat.id)
    else:
        msg = bot.reply_to(message, "Неверный статус")
    print(f"id={message.from_user.id} user={message.from_user.first_name} status={status}: {message.text}")
    status_id=message.from_user.first_name
    #print (status_id) 

@bot.message_handler(content_types=["text"])
def enter_user(message):
    #print(f" status={status}: {message.text}")
    if status == 6:
      bot.send_message(message.chat.id, 'Кому вы передали ключ?')  
      global user_key
      user_key=message.text 
      if len(message.text) < 2 or message.text == "status" or message.text == "/help":
          bot.register_next_step_handler(message, enter_user)
      else:
          bot.send_message(message.chat.id, 'Запомнил.')
        
bot.polling(none_stop=True, interval=0)
