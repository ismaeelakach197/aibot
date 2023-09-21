import telebot
import sqlite3
import requests

API_KEY = "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"
BOT_KEY = "6059146214:AAH0t4S8tLcDL81HrUFnU4GIiwhbO8GraXU"
types = telebot.types
bot = telebot.TeleBot(BOT_KEY)
MY_CHAT_ID = 156956400
spchars = ['\\', '/', ':', '*', "?", "'", "<", ">", "|"]

# def generate_response(message):
#     openai.api_key = API_KEY
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=message.text,
#         temperature=0.1,
#         max_tokens=1024,
#         top_p=1,
#         frequency_penalty=0.2,
#         presence_penalty=0,
#         stop=["\"\"\""]
#     )
#     print(response)
#     if message.chat.id != MY_CHAT_ID:
#         bot.send_message(MY_CHAT_ID, str(response['choices'][0].text))
#         add(message, str(response['choices'][0].text))
#     return str(response['choices'][0].text)
def add(message, resp):
    conn = sqlite3.connect('chats.db')
    c = conn.cursor()

    c.execute(f"INSERT INTO activity (first_name, last_name, username, chatid, activity) VALUES('{message.chat.first_name}', '{message.chat.last_name}', '{message.chat.username}', '{message.chat.id}', '{message.text}___{resp}')")
    conn.commit()
    conn.close()

@bot.message_handler(commands=['start'])
def start(message):
    print("started")
    bot.send_message(message.chat.id, "Welcome, Im Artificial intelligence bot ready for your questions \n try /ask to start chating")
def handle(message):
    print("update")
@bot.message_handler(commands=['ask'])
def ask(message):

    print(message.text)
    send_req = bot.send_message(message.chat.id, "Send Your Question")
    bot.register_next_step_handler(send_req, get_question)

def get_question(message):
    if message.chat.id != MY_CHAT_ID:
        bot.send_message(MY_CHAT_ID, str(f"{message.text}{message.chat}"))
    reply = bot.reply_to(message, "Generating Response...")
    getres(message, reply)


url = "https://robomatic-ai.p.rapidapi.com/api"
def getres(message, reply):
    print(message.text)
    payload = {
        "in": message.text,
        "op": "in",
        "cbot": "1",
        "SessionID": "RapidAPI1",
        "cbid": "1",
        "key": "RHMN5hnQ4wTYZBGCF3dfxzypt68rVP",
        "ChatSource": "RapidAPI",
        "duration": "1"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "1264c3a6femsh23356ae064e1601p157451jsnfcc82b459708",
        "X-RapidAPI-Host": "robomatic-ai.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)
    bot.delete_message(reply.chat.id, reply.id)
    json = response.json()
    answer = json['out']
    fanswear = ''
    for t in answer:
        if t not in spchars:
            fanswear += t
    print(f"answer   {fanswear}")
    add(message, fanswear)
    bot.send_message(message.chat.id, answer)


bot.set_update_listener(handle) #register listener
bot.polling(True)
