from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.get("/generate_image")
def generate_image():
    print("inside generate image")
    # Get the prompt from the request JSON
    prompt = request.json['prompt']

    # Call the Hugging Face API for inference
    response = requests.post(
        'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1',
        headers={'Authorization': 'Bearer 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'},
        json={'inputs': prompt}
    )

    # Get the image content from the response
    image_content = response.content

    # Return the image as a response
    return jsonify({'image': image_content})
