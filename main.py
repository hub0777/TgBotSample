import telebot

bot = telebot.TeleBot(TG_TOKEN)
print('hey')

#start command
@bot.message_handler(commands=['start'])
def start_message(message):
    user = message.chat.id
    bot.send_message(user,'Hello \n you cracket!!! ')

#main code
@bot.message_handler(content_types=['text'])
def send_text(message):
    user = message.chat.id
    
    if message.text == "help":
        bot.send_message(user,'⛄⛄⛄⛄⛄ cracker ⛄⛄⛄⛄⛄')

    elif message.text == '🤍':
        bot.send_message(user, '⛄⛄⛄⛄')

    elif message.text == 'bye':
        bot.send_message(user, 'well')
        bot.send_message(user, 'see you')
    else:
        bot.send_message(message.chat.id, 'hahaha ¯\_(ツ)_/¯ ')

bot.infinity_polling()
