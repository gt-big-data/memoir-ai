import base64
from openai import OpenAI
import os 
from dotenv import load_dotenv
import img_to_vector

def generate_embedding(image_description):
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-large",  # Use the appropriate model
        input=image_description  # Pass in the list of descriptions
    )
    
    return len(response.data[0].embedding)

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def generate_descriptions(image_paths):
    descriptions = []
    for path in image_paths:
       descriptions.append(img_to_vector.generate_description(path))
    return descriptions
    
def load_image_paths():
    #Use below if changing sample images
    #return ["/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/san-francisco-family-photo.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/pizza-in-ny.png", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/mona-lisa.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/kids_playing_on_playground-1-1084x610.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/1000023034.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/1000022876.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/1000022871.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/1000022805.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/1000022778.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/1000022772.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/1000022538.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/1000022462.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/1000022437.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/1000022230.jpg", "/Users/amogh/Library/CloudStorage/OneDrive-Personal/GT/BDBI/memoir-ai/few-shot-imgs/360_F_381776941_7cPXNVNze3bKDxilLJPzOCSaQIckPqWN.jpg"]
    return ['The image shows a family—two adults and a child—posing on a sandy beach. The woman is holding the child, and they are all smiling at the camera. A dog is walking in the sand nearby. In the background, there is a view of the iconic Golden Gate Bridge with hills and water under a partly cloudy sky.', 'The image shows a group of young people in a pizza restaurant enjoying pizza slices. They appear to be having a good time, smiling and talking with each other. The walls are decorated with photos and memorabilia. A tray with a whole pizza is visible on the table. The atmosphere is lively and casual.', 'The image shows a large crowd gathered in a museum or gallery, focused on a central painting. Many people are holding up phones and tablets, taking photos or videos of the artwork. The walls of the room are dark, and several other framed paintings are visible on the walls.', 'The image shows a group of five children playing together on a playground. One child is using a wheelchair, and the others are engaging with play equipment that includes slides and climbing structures. The scene is outdoors, with trees visible in the background, and the children appear to be having fun and interacting with each other.', 'The image shows a cityscape with several modern buildings featuring reflective glass exteriors. In the foreground, there is a parking lot and trees lining a street. Raindrops are visible on the window through which the photo is taken, suggesting rainy or overcast weather. The sky is cloudy, contributing to the overall gray tone of the scene.', 'The image shows a group of six people gathered around a dining table, which features a large roasted turkey as a centerpiece. The people appear cheerful, and some are holding glasses of wine. Behind them is a wooden cabinet with glass doors, displaying various decorative items like plates and other collectibles. The scene suggests a festive or celebratory meal, possibly a holiday gathering.', 'The image features a roasted turkey with a golden-brown crust, stuffed with a savory filling. The turkey is placed on a platter surrounded by pieces of yellow squash and green beans. In the background, there is a bottle (possibly wine or a spirit) and two glasses partially filled with a white beverage. The setting appears to be a dining table, suggesting a festive or special meal.', 'The image shows the interior of a large retail store, likely an electronics department. There are several laptops displayed on a counter with pricing information and signage. In the background, there are large Sony Bravia televisions on display. The store has high ceilings with bright lighting. Two people are in the scene—one is pushing a shopping cart past the laptops, and another is looking at one of the laptops on display.', 'The image shows a plate of food featuring a variety of meats, including roasted pork and sliced chicken. The dish is garnished with chopped green onions. It also includes a serving of boiled egg and a mixture of cooked vegetables on the side, all served over a bed of rice. The setting appears to be a casual dining environment.', 'The image shows a highway scene taken from inside a vehicle. There is a red SUV to the left and a flatbed tow truck to the right in adjacent lanes. The view includes other cars on the road ahead and a clear blue sky. On the right side, there are buildings, with one prominently displaying "NCR." The dashboard of the vehicle taking the picture shows a navigation screen.', "The image shows a sleek black car parked in a parking lot. The car features a streamlined design with a smooth, glossy finish and is positioned slightly angled to the camera. In the background, there are green bushes and trees, along with some power lines and poles. A trash can is visible on the right side of the image. The scene is lit by daylight, suggesting it's taken during the day.", 'The image depicts a scenic landscape featuring a river surrounded by autumn foliage. The trees, displaying vibrant shades of green, yellow, and orange, frame the view. In the background, rolling hills can be seen under a partly cloudy sky. The setting appears to be a natural, tranquil environment.', 'The image shows a scenic view of a wide river with gentle ripples on its surface. It is surrounded by lush forested hills displaying autumn colors, including green, yellow, and orange foliage. The sky above is partly cloudy with patches of blue sky visible. The reflection of the clouds and trees is visible on the water, adding to the picturesque and tranquil atmosphere.', "The image shows a nighttime view of a high-rise residential building. The building is illuminated with lights from the windows, revealing various levels and balconies. At the bottom, there's a pool with surrounding deck chairs, and in the foreground are a few trees. In the background, more buildings and streetlights are visible, hinting at an urban setting.", 'The image depicts two children playing on a sandy beach by the ocean. The boy, wearing a light blue hat and T-shirt, is focused on building sand structures with colorful buckets and tools. The girl, in a pink shirt and yellow sunglasses, is also engaged in building sandcastles. The scene is set against a clear sky and calm sea, conveying a sunny, relaxed beach day.']
def get_optimal_query(user_query):
    image_paths = load_image_paths()
    #Use below if changing sample images
    #descriptions = generate_descriptions(image_paths)
    #Use below if already loaded sample descriptions and images
    descriptions = image_paths 
    system_prompt = f"{descriptions} The given list contains detailed descriptions of images. Use these descriptions and a user-inputted query to come up with an optimized version of the user-inputted query. This optimized query will be converted to a vector embedding which will be used to find relevant photos in a vector database."
    client = OpenAI()
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": system_prompt}, {"role": "system", "content": user_query}],
    temperature=0.7
    )
    
    return img_to_vector.generate_embedding(response.choices[0].message.content)


#Load environment variables from .env 
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

print(len(get_optimal_query("show me photos with scenic views")))
