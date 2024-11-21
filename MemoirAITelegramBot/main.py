import os
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import requests

from img_to_vector import encode_image, generate_embedding, generate_description, get_embeddings
from optimized_query import generate_descriptions, get_optimal_query
from vectordb import create_faiss_database, query_faiss_database, add_to_metadata

load_dotenv()







FAISS_INDEX_PATH = "faiss_index_3072.index"







imgur_client_id = os.getenv('IMGUR_CLIENT_ID')
imgur_client_secret = os.getenv('IMGUR_CLIENT_SECRET')
TOKEN = os.getenv('TOKEN')
BOT_USERNAME: Final = "@MemoirAIBot"

IMAGE_DIRECTORY = "downloaded_images"
os.makedirs(IMAGE_DIRECTORY, exist_ok=True)

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

    if any(tag in text.strip() for tag in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.HEIC']):
        await handle_file_path(update, context)
        return

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

#upload user inputted images to a local directory called downloaded_images in local machine
async def handle_images(update: Update, context: CallbackContext) -> None:
    paths = []
    for photo in update.message.photo:
        highest_res_photo = update.message.photo[-1]
        photo_file = await highest_res_photo.get_file()
        local_path = os.path.join(IMAGE_DIRECTORY, f"{update.message.chat.id}_{photo_file.file_unique_id}.jpg")
        await photo_file.download_to_drive(local_path)
        paths.append(local_path)
    if paths:
        await update.message.reply_text("Images stored! Here are the paths:\n" + "\n".join(paths))
    else:
        await update.message.reply_text("No images were processed.")





# async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user_id = update.message.chat.id
#     photos = update.message.photo

#     # Save the highest-resolution image
#     highest_res_photo = photos[-1]
#     photo_file = await highest_res_photo.get_file()
#     local_path = os.path.join(IMAGE_DIRECTORY, f"{user_id}_{photo_file.file_unique_id}.jpg")
#     await photo_file.download_to_drive(local_path)

#     # Generate description and embedding
#     await update.message.reply_text("Processing your image...")
#     description = generate_description(local_path)
#     await update.message.reply_text(description)
#     return

async def handle_image(update: Update, context: CallbackContext):
    # Save image locally
    file = await update.message.photo[-1].get_file()
    image_path = os.path.join(IMAGE_DIRECTORY, f"{update.message.photo[-1].file_id}.jpg")
    await file.download_to_drive(image_path)

    # Simulate generating an embedding for the image description (replace with actual model)
    await update.message.reply_text("Processing your image...")
    description = generate_description(image_path)
    embedding = generate_embedding(description)
    
    new_entry = (str(len(os.listdir(IMAGE_DIRECTORY))), image_path)
    # Store the image path and embedding
    data = [(image_path, embedding)]
    # if not os.path.exists("metadata_3072.json"):
    create_faiss_database(data)
    # else:
    #     print("HERE NOW")
    #     add_to_metadata(new_entry, data)

    await update.message.reply_text("Image received and stored! You can now query for similar images.")

async def handle_query(update: Update, context: CallbackContext):
    print(os.path.exists("metadata_3072.json"))
    user_query = update.message.text
    user_id = update.message.chat.id

    query_embedding = generate_embedding(user_query)  # Get the query embedding

    # Query the FAISS index for similar images
    top_images = query_faiss_database(query_embedding)

    # Prepare the response
    # response = "Top similar images:\n"
    for idx, (image_path, similarity) in enumerate(top_images):
        # response += f"{idx + 1}: {image_path} (similarity: {similarity:.4f})\n"
        await context.bot.send_photo(chat_id=user_id, photo=image_path)
            
    # await update.message.reply_text(response)






async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


async def handle_file_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    text = update.message.text.strip()

    file_paths = text.strip().split(',')
    print(file_paths)
    returned = False
    
    for file_path in file_paths:
        if not os.path.exists(file_path.strip()):
            await context.bot.send_message(chat_id=user_id, text="The file does not exist.")
            return
        
        try:
            with open(file_path.strip(), 'rb') as file:
                await context.bot.send_photo(chat_id=user_id, photo=file)
            returned = True
        except Exception as e:
            await context.bot.send_message(chat_id=user_id, text=f"Error: {e}")

    if returned:
        if len(file_paths) == 1:
            await context.bot.send_message(chat_id=user_id, text="Image successfully retrieved!")
        else:
            await context.bot.send_message(chat_id=user_id, text="Images successfully retrieved!")


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Testing
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_images))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_file_path))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
