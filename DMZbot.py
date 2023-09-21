import telebot

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
status="4"
status_id="None"
bot = telebot.TeleBot('TOKEN');

keys = ["0","1","2","3","4","5","/help"]

def keyboard():
    markup = ReplyKeyboardMarkup(row_width=4)
    row = [KeyboardButton(x) for x in keys[:10]]
    markup.add(*row)
    markup.add(KeyboardButton("status"))
    markup.add(KeyboardButton("close keyboard"))

    return markup
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
status- показать статус
    """,reply_markup=keyboard())

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global status
    global status_id
    status_id=message.from_user.first_name
    #print(f"id={message.from_user.id} user={message.from_user.first_name} status={status}")
    if message.text == "close keyboard":
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id,"Done with Keyboard",reply_markup=markup)
    elif message.text == "/start" or message.text == "/help":
        bot.register_next_step_handler(message.text, send_welcome(message.text))
    elif message.text == "status":
        if status == 0:
            tmp_str=str(f"Ключ на ресепшене")
            bot.send_message(message.chat.id, tmp_str)
        if status == 1:
            tmp_str=str(f"Ключ у {status_id} в офисе")
            bot.send_message(message.chat.id, tmp_str)
        if status == 2:
            tmp_str=str(f"Ключ у {status_id} в ДЗ")
            bot.send_message(message.chat.id, tmp_str)
        if status == 3:
            tmp_str=str(f"ДЗ закрыт на ключ и СКУД")
            bot.send_message(message.chat.id, tmp_str)
        if status == 4:
            tmp_str=str(f"ДЗ закрыт на ключ, без СКУД")
            bot.send_message(message.chat.id, tmp_str)
        if status == 5:
            tmp_str=str(f"ДЗ открыт")
            bot.send_message(message.chat.id, tmp_str)
        #elif status == 4:
            #bot.send_message(message.chat.id,message.text)
            #bot.reply_to(message, "взял ключ, снял с охраны, открыл ДЗ, нахожусь в ДЗ")
    elif message.text == "0":
        msg = bot.reply_to(message, "Ключ на ресепшене")
        status=0
        #bot.reply_to(message, status)
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "1":
        msg = bot.reply_to(message, "Ключ у меня в офисе")
        status=1
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "2":
        msg = bot.reply_to(message, "Ключ у меня в ДЗ")
        status=2
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "3":
        msg = bot.reply_to(message, "ДЗ закрыт на ключ и СКУД")
        status=3
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "4":
        msg = bot.reply_to(message, "ДЗ закрыт на ключ, без СКУД")
        status=4
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "5":
        msg = bot.reply_to(message, "ДЗ открыт")
        status=5
        #bot.register_next_step_handler(msg, show_status)
        #msg = bot.reply_to(message, status)
    else:
        msg = bot.reply_to(message, "Неверный статус")
    print(f"id={message.from_user.id} user={message.from_user.first_name} status={status}")
    status_id=message.from_user.first_name
    #print (status_id) 

bot.polling(none_stop=True, interval=0)
