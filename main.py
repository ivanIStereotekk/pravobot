from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
import telebot
import environ
from pathlib import Path
import os
from utils.bot_utils import callback_data, START_BUTTON_MARKUP, how_to_text, reward_text, about_text,start_text
import time


env = environ.Env(DEBUG=(bool,False))
BASE_DIR = Path(__file__).resolve().parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))




# BOT Instance
BOT = telebot.TeleBot(token=env('TELEGRAM_TOKEN'))




# Pinecone

pc = Pinecone(api_key=env('PINECONE_API_KEY'))



assistant = pc.assistant.Assistant(assistant_name=env('ASSISTANT'))


@BOT.callback_query_handler(func=lambda call:True)
def callback_query(call):
    
    BOT.answer_callback_query(call.id,callback_data[call.data],show_alert=False)
    match call.data:
        case 'howto': 
            BOT.send_message(call.message.chat.id,text=how_to_text)
        case 'about': 
            BOT.send_message(call.message.chat.id,text=about_text)
        case _:
            pass
        
        


@BOT.message_handler(commands=['start', 'help'])
def send_welcome(message):
	BOT.send_message(chat_id=message.chat.id, text=start_text ,reply_markup=START_BUTTON_MARKUP)

         


@BOT.message_handler(func=lambda m: True)
def handle_message(user_message):
    message = Message(role="user", content=user_message.text)
    response = assistant.chat(messages=[message])
    BOT.reply_to(message=user_message,text=str(response.message['content']))
    time.sleep(15)
    BOT.send_message(user_message.chat.id,text=reward_text)




if __name__=='__main__':
    BOT.infinity_polling()




