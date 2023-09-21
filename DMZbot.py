import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
status="4"
bot = telebot.TeleBot('TOKEN');

keys = ["0","1","2","3","4","5","status"]

def keyboard():
    markup = ReplyKeyboardMarkup(row_width=4)
    row = [KeyboardButton(x) for x in keys[:10]]
    markup.add(*row)
    markup.add(KeyboardButton("/help"))
    markup.add(KeyboardButton("✅close keyboard"))

    return markup
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    #bot.send_message(message.from_user.id,"",reply_markup=keyboard())
    bot.send_message(message.from_user.id, """\
0 - ДЗ открыт
1 - взял ключ, снял с охраны, открыл ДЗ, нахожусь в ДЗ
2 - ДЗ закрыт
3 - ушел из ДЗ, закрыл на ключ, сдал ключ охраннику
4 - ДЗ на охране
5 - ушел из ДЗ, закрыл на ключ, поставил на охрану, сдал ключ
6 - показать статус
    """,reply_markup=keyboard())

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global status
    
    if message.text == "✅close keyboard":
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id,"Done with Keyboard",reply_markup=markup)
    elif message.text == "/start" or message.text == "/help":
        bot.register_next_step_handler(message.text, send_welcome(message.text))
    elif message.text == "status":
        if status == 0:
            bot.send_message(message.chat.id, "ДЗ открыт")
        if status == 1:
            bot.send_message(message.chat.id, "взял ключ, снял с охраны, открыл ДЗ, нахожусь в ДЗ")
        if status == 2:
            bot.send_message(message.chat.id, "ДЗ закрыт")
        if status == 3:
            bot.send_message(message.chat.id, "ушел из ДЗ, закрыл на ключ, сдал ключ охраннику")
        if status == 4:
            bot.send_message(message.chat.id, "ДЗ на охране")
        if status == 5:
            bot.send_message(message.chat.id, "ушел из ДЗ, закрыл на ключ, поставил на охрану, сдал ключ")
        #elif status == 4:
            #bot.send_message(message.chat.id,message.text)
            #bot.reply_to(message, "взял ключ, снял с охраны, открыл ДЗ, нахожусь в ДЗ")
    elif message.text == "0":
        msg = bot.reply_to(message, "ДЗ открыт")
        status=0
        #bot.reply_to(message, status)
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "1":
        msg = bot.reply_to(message, "взял ключ, снял с охраны, открыл ДЗ, нахожусь в ДЗ")
        status=1
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "2":
        msg = bot.reply_to(message, "ДЗ закрыт")
        status=2
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "3":
        msg = bot.reply_to(message, "ушел из ДЗ, закрыл на ключ, сдал ключ охраннику")
        status=3
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "4":
        msg = bot.reply_to(message, "ДЗ на охране")
        status=4
        #bot.register_next_step_handler(msg, show_status)
    elif message.text == "5":
        msg = bot.reply_to(message, "ушел из ДЗ, закрыл на ключ, поставил на охрану, сдал ключ")
        status=5
        #bot.register_next_step_handler(msg, show_status)
        #msg = bot.reply_to(message, status)
    else:
        msg = bot.reply_to(message, "Неверный статус")
    print(f"id={message.from_user.id} user={message.from_user.first_name} status={status}")
        
bot.polling(none_stop=True, interval=0)
