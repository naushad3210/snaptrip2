from flask import Flask, request, jsonify, send_file
from PIL import Image
import requests
# You can access the image with PIL.Image for example
import io

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "Chair", "price": 15.99}]}]


@app.get("/store")
def get_stores():
    return {"stores": stores}


@app.get("/hello/<string:prompt>")
def get_hello():
    return {"hello": "world"}


@app.get("/hello")
def get_hello1():
    return {"hello": "world"}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404


@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404


@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404


@app.post("/generate_image")
def generate_image():
    print("inside generate image")
    # Get the prompt from the request JSON
    prompt = request.json['prompt']
    print("prompt== " + prompt)

    # Call the Hugging Face API for inference
    response = requests.post(
        'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1',
        headers={'Authorization': 'Bearer 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'},
        json={'inputs': prompt}
    )

    # Get the image content from the response
    image_content = response.content

    # Create a file-like object for the image content
    image_stream = io.BytesIO(image_content)

    # Return the image as a file attachment in the response
    return send_file(image_stream, mimetype='image/jpeg')
