from typing import Final
import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
   
    TOKEN: Final = os.getenv('TELEGRAM_TOKEN', '7640732725:AAEE_tMsusP4Ckut5MnPOpuaF9b4Xgk9oJo')
    BOT_USERNAME: Final = os.getenv('BOT_USERNAME', '@memoirAI_bot')
    

    IMGUR_CLIENT_ID: Final = os.getenv('IMGUR_CLIENT_ID', '8c08be70f5cc908')
    IMGUR_API_URL: Final = "https://api.imgur.com/3"