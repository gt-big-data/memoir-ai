from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')
print(f"Token loaded: {token}")