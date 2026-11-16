import os
import random

import openai
import telebot
from dotenv import load_dotenv

# load the secret keys from the .env file
load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TG_TOKEN)

# read countries.txt into a list, one country per line
countries = []
folder = os.path.dirname(os.path.abspath(__file__))
countries_path = os.path.join(folder, "countries.txt")
with open(countries_path, "r", encoding="utf-8") as file:
    for line in file:
        country = line.strip()
        if country != "":
            countries.append(country)

print("bot is running, loaded", len(countries), "countries")


# ask the AI a question and return its answer as text
def ask_ai(question):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant inside a Telegram bot. Keep answers short."},
                {"role": "user", "content": question}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        answer = response.choices[0].message.content
        if answer is None or answer.strip() == "":
            return "I didn't get an answer, try asking again."
        return answer.strip()
    except openai.OpenAIError as e:
        print("OpenAI API error:", e)
        return "Sorry, I can't answer that right now."


# /start command
@bot.message_handler(commands=["start"])
def start_message(message):
    user = message.chat.id
    text = "Hello! Here's what I can do:\n"
    text = text + "/number - random number from 1 to 100\n"
    text = text + "/country - random country\n"
    text = text + "Anything else you type, I answer as an AI assistant."
    bot.send_message(user, text)


# /number command
@bot.message_handler(commands=["number"])
def number_message(message):
    user = message.chat.id
    number = random.randint(1, 100)
    bot.send_message(user, "Your random number is " + str(number))


# /country command
@bot.message_handler(commands=["country"])
def country_message(message):
    user = message.chat.id
    country = random.choice(countries)
    bot.send_message(user, "Your random country is " + country)


# every other text message goes to the AI
@bot.message_handler(content_types=["text"])
def send_text(message):
    user = message.chat.id
    bot.send_chat_action(user, "typing")
    answer = ask_ai(message.text)
    bot.send_message(user, answer)


bot.infinity_polling()