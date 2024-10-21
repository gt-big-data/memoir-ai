import os
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import requests
from io import BytesIO
import re

load_dotenv()

imgur_client_id = os.getenv('IMGUR_CLIENT_ID')
imgur_client_secret = os.getenv('IMGUR_CLIENT_SECRET')
TOKEN = os.getenv('TOKEN')
BOT_USERNAME: Final = "@MemoirAIBot"

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello and thank you for using MemoirAI, how may I assist you?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is MemoirAI. Please input an image to upload to imgur or a link to imgur image you would like displayed.")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" and "memoirai" in processed:
        return "Hey there, I am an intelligent memory companion that intuitively stores, tags, and retrieves images, notes, and videos on cloud"
    
    if "hello" in processed:
        return "Hey!"

    if "how are you" in processed:
        return "I am good"
    
    if "memoirai" in processed:
        return "I am an intelligent memory companion that intuitively stores, tags, and retrieves images, notes, and videos on cloud"
    
    if "help" in processed:
        return "Just send an image and I'll handle the rest"
    
    return "Sorry, I don't understand"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if 'imgur.com' in text:
        imgur_link = text.strip()
        await update.message.reply_text('Processing your Imgur link...')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)

async def handle_image(update: Update, context: CallbackContext) -> None:
    photo_file = await update.message.photo[-1].get_file()

    photo_bytes = await photo_file.download_as_bytearray()

    imgur_link = upload_to_imgur(photo_bytes)

    await update.message.reply_text(f"Image uploaded! Here is your link: {imgur_link}")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")



# Helper Methods
def upload_to_imgur(image_file: bytes) -> str:
    headers = {"Authorization": f"Client-ID {imgur_client_id}"}
    response = requests.post('https://api.imgur.com/3/image', headers=headers, files={"image": image_file})
    
    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        return "Failed to upload image."
    


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
