import base64
from openai import OpenAI
import os 
from dotenv import load_dotenv

def generate_embedding(image_description):
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-large",  # Use the appropriate model
        input=image_description  # Pass in the list of descriptions
    )
    
    return response.data[0].embedding

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def generate_description(image_path):
    client = OpenAI()
    base64_image = encode_image(image_path)
    try:
        completion = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=400,
        messages=[
            {
                "role": "system",
                "content": [
                    {"type": "text", 
                    "text": 
                        'You are a helpful assistant who briefly describes key features of an image. This description should be descriptive enough for someone who has never seen the picture to visualize it.'
                    },
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f'data:image/jpeg;base64,{base64_image}'
                        }
                    },
                ],
            }
            ],
        )

        return completion.choices[0].message.content
    except Exception as e:
        return e
    
def get_embeddings(image_paths):
    embeddings = []
    for image_path in image_paths:
        #Generate a description of the image
        description = generate_description(image_path)
        if(type(description) != type(" ")):
            return description
        
        #Generate an embedding for the description
        embedding = generate_embedding(description)
        embeddings.append({image_path:embedding})
    return embeddings

#Load environment variables from .env 
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

#print(generate_description("/Users/amogh/Desktop/A_family_photograph_of_people_jumping_in_Marin_County,_California,_USA_with_the_Golden_Gate_Bridge_in_the_background.jpg"))
#print(generate_embedding("The image shows four people near the Golden Gate Bridge. Three of them are jumping into the air with their arms raised, while the fourth person, a child, is crouching down. The iconic red bridge spans the background, with a view of the water and cityscape beyond. The sky is clear and blue."))
#print(generate_description("/Users/amogh/Desktop/Rajagopal-Amogh-SIGNATURE_THEME.pdf"))
