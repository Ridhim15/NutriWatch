import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import request, jsonify  # Importing request and jsonify from Flask

load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.environ["API_KEY"])

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,  # type: ignore
)

def extract_data():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    image_path = os.path.join("uploads", image.filename)

    # Ensure the uploads directory exists
    os.makedirs("uploads", exist_ok=True)

    try:
        image.save(image_path)  # Save the uploaded image
    except Exception as e:
        return jsonify({"error": f"Failed to save image: {str(e)}"}), 500

    # Process the image using the Google Generative AI script
    try:
        uploaded_file = upload_to_gemini(image_path, mime_type="image/jpeg")

        # Start chat session with the model
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "You are LabelDataExtractor, an expert in extracting information from product label images and providing structured insights in JSON format.\n\nYou will be given an image by the user that contains labeled data (like ingredients, nutritional information, etc.). Your main task is to extract all relevant details from the label, especially focusing on the ingredients, and return the information in the following JSON structure:\n\n{\n  \"ProductName\": \"Extracted Product Name\",\n  \"Ingredients\": [\n    \"Ingredient 1\",\n    \"Ingredient 2\",\n    \"Ingredient 3\"\n    // ... more ingredients\n  ],\n  \"AdditionalDetails\": {\n\"Allergens \": [\"Identify all allergens from the ingredients and mentioned allergens\"]\n    \"ServingSize\": \"Extracted Serving Size\",\n    \"Calories\": \"Extracted Calories\",\n    \"OtherInfo\": \"Any other important information extracted\"\n  }\n}\n\nRemember:\nExtract all relevant data from the label.\nThe main focus is on extracting the ingredients.\nOutput the data strictly in JSON format.",
                        uploaded_file,
                    ],
                },
            ]
        )

        # Send a prompt (provide a minimal non-empty string)
        response = chat_session.send_message("Please extract information from the image.")

        # Return the JSON response from the model
        return jsonify(response.text)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
