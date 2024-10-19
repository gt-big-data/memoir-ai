from flask import Flask, request, jsonify
from api_client import ImgurClient
from config import Config

app = Flask(__name__)

config = Config()
imgur_client = ImgurClient(config.IMGUR_CLIENT_ID, config.IMGUR_API_URL)

@app.route('/upload_text', methods=['POST'])
def upload_text():
    data = request.json
    text = data.get('text')
    
    if text:
        result = imgur_client.upload_text(text)
        return jsonify(result)
    else:
        return jsonify({"error": "No text provided"}), 400

@app.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files['image']
    
    if image:
        image_data = image.read()
        result = imgur_client.upload_image(image_data)
        return jsonify(result)
    else:
        return jsonify({"error": "No image provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
