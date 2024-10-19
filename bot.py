from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import aiohttp
from config import Config
from api_client import ImgurClient


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MemoirBot:
    def __init__(self):
        self.config = Config()
        self.imgur_client = ImgurClient(
            self.config.IMGUR_CLIENT_ID,
            self.config.IMGUR_API_URL
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Hi! Send me text or images to store.')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('You can send either text or images.')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            if update.message.text:
                logger.info("Handling text message")
                result = await self.imgur_client.upload_text(update.message.text)
                await update.message.reply_text(result['message'])
                
            elif update.message.photo:
                logger.info("Handling photo message")
       
                photo = update.message.photo[-1]
                photo_file = await context.bot.get_file(photo.file_id)
                

                async with aiohttp.ClientSession() as session:
                    async with session.get(photo_file.file_path) as response:
                        photo_content = await response.read()
                

                result = await self.imgur_client.upload_image(photo_content)
                await update.message.reply_text(result['message'])

        except Exception as e:
            error_message = f"Error processing message: {str(e)}"
            logger.error(error_message)
            await update.message.reply_text(error_message)

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f"Update {update} caused error {context.error}")

    def run(self):
        app = Application.builder().token(self.config.TOKEN).build()


        app.add_handler(CommandHandler('start', self.start_command))
        app.add_handler(CommandHandler('help', self.help_command))
        app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        app.add_handler(MessageHandler(filters.PHOTO, self.handle_message))
        app.add_error_handler(self.error_handler)

        logger.info("Starting bot...")
        app.run_polling(poll_interval=3)

if __name__ == '__main__':
    bot = MemoirBot()
    bot.run()