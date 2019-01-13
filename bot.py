import telebot
from telebot.types import Message
import random
from flask import Flask, request
import os


bot_token = '672782236:AAGoWrNm-TtgElTe8Lb5jLTJvgm4yVuk6Wo'
bot = telebot.TeleBot(token=bot_token)
server = Flask(__name__)

picfile = 'pics.txt'
audiofile = 'audio.txt'
quotefile = 'quotes.txt'

with open(picfile) as p, open(audiofile) as a, open(quotefile) as q:
    plines = p.readlines()
    alines = a.readlines()
    qlines = q.readlines()



@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, '/zetti - pics\n/baghi - audio\n/donzetti - testo')

@bot.message_handler(commands=['zetti'])
def send_rand_photo(message):
    photo = random.choice(plines)
    bot.send_photo(message.chat.id, photo, random.choice(qlines))

@bot.message_handler(commands=['baghi'])
def send_rand_audio(message):
    audio = random.choice(alines)
    bot.send_voice(message.chat.id, audio)

@bot.message_handler(commands=['donzetti'])
def send_rand_quote(message):
    quote = random.choice(qlines)
    bot.send_message(message.chat.id, quote)

@bot.message_handler(func=lambda msg: msg.text is not None and 'brother' in msg.text)
def at_answer(message):
    quote = random.choice(qlines)
    bot.reply_to(message, quote)


    

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://vast-stream-79139.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
