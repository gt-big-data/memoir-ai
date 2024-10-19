import aiohttp
import logging
from typing import Optional, Union, Dict

logger = logging.getLogger(__name__)

class ImgurClient:
    def __init__(self, client_id: str, api_url: str):
        self.client_id = client_id
        self.api_url = api_url
        self.headers = {"Authorization": f"Client-ID {client_id}"}

    async def upload_text(self, text: str) -> Dict:

        async with aiohttp.ClientSession() as session:
            try:
                data = {
                    'title': 'Text Note',
                    'description': text
                }
                async with session.post(
                    f'{self.api_url}/gallery/image',
                    headers=self.headers,
                    json=data
                ) as response:
                    result = await response.json()
                    logger.info(f"Imgur text upload response: {result}")
                    return {
                        'success': True,
                        'message': "testapi.com/put text api called",
                        'data': result
                    }
            except Exception as e:
                logger.error(f"Error uploading text to Imgur: {e}")
                return {
                    'success': False,
                    'message': f"Error uploading text: {str(e)}"
                }

    async def upload_image(self, image_data: bytes) -> Dict:

        async with aiohttp.ClientSession() as session:
            try:
                data = aiohttp.FormData()
                data.add_field('image', image_data)
                
                async with session.post(
                    f'{self.api_url}/image',
                    headers=self.headers,
                    data=data
                ) as response:
                    result = await response.json()
                    logger.info(f"Imgur image upload response: {result}")
                    return {
                        'success': True,
                        'message': "testapi.com/put image api called",
                        'data': result
                    }
            except Exception as e:
                logger.error(f"Error uploading image to Imgur: {e}")
                return {
                    'success': False,
                    'message': f"Error uploading image: {str(e)}"
                }