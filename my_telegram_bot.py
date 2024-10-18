from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
# TOKEN = os.getenv('TOKEN')
# BOT_USERNAME = os.getenv('BOT_USERNAME')
TOKEN: Final = '7640732725:AAEE_tMsusP4Ckut5MnPOpuaF9b4Xgk9oJo'
BOT_USERNAME: Final = '@memoirAI_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('hi thanks for chatting with me')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('You can either input a text or image you want to find')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('custom command')

def handle_responses(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'hi'
    if 'how are you' in processed:
        return 'i am good'
    # handle responses

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('handle message')
    message_type: str = update.message.chat.type
    photo_bool: bool = update.message.photo != ()
    text_bool : bool = update.message.text != None
    # print(type(update.message.photo))
    # print(update.message.text)
    # print(photo_bool)
    # print('photo')
    # print(text_bool)
    # print('text')
    #text: str = update.message.text
    #response: str = handle_responses(text)

    if text_bool == True:
        response = 'text api called'
    elif photo_bool == True: 
        response = 'photo api called'

    print(f'User ({update.message.chat.id}) in {message_type}: "{response}"')

    await update.message.reply_text(response)
    print('message handled')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    #app = Application(token=TOKEN)
    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    #messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_message))
    app.add_handler(MessageHandler(filters.Command, custom_command))
    app.add_error_handler(error)

    print('polling')
    app.run_polling(poll_interval = 3)
    #app.run()




print('hello')

#imgur api
#8c08be70f5cc908 client ID
#f924c6d1d2ea1a85908113259cdfd82a30e162f5 secret
#5bcdcf31bec025e449d2d072f04d799315b5a122 access token