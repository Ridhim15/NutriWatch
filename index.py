from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response, send_from_directory
import os

# Configure Google Generative AI
# genai.configure(api_key="YOUR_API_KEY_HERE")

# def upload_to_gemini(path, mime_type=None):
#     """Uploads the given file to Gemini."""
#     file = genai.upload_file(path, mime_type=mime_type)
#     print(f"Uploaded file '{file.display_name}' as: {file.uri}")
#     return file

# # Create the model configuration
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "max_output_tokens": 8192,
#     "response_mime_type": "application/json",
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-flash",
#     generation_config=generation_config,
# )

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

# @app.route('/status', methods=['GET'])
# def status():
#     return "Server is running"

# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image file provided"}), 400
    
#     image = request.files['image']
#     image_path = os.path.join("uploads", image.filename)
#     image.save(image_path)  # Save the uploaded image
    
#     # Process the image using the Google Generative AI script
#     try:
#         uploaded_file = upload_to_gemini(image_path, mime_type="image/jpeg")
        
#         # Start chat session with the model
#         chat_session = model.start_chat(
#             history=[
#                 {
#                     "role": "user",
#                     "parts": [
#                         "You are LabelDataExtractor, an expert in extracting information from product label images and providing structured insights in JSON format.\n\nYou will be given an image by the user that contains labeled data (like ingredients, nutritional information, etc.). Your main task is to extract all relevant details from the label, especially focusing on the ingredients, and return the information in the following JSON structure:\n\n{\n  \"ProductName\": \"Extracted Product Name\",\n  \"Ingredients\": [\n    \"Ingredient 1\",\n    \"Ingredient 2\",\n    \"Ingredient 3\"\n    // ... more ingredients\n  ],\n  \"AdditionalDetails\": {\n\"Allergens \": [\"Identify all allergens from the ingredients and mentioned allergens\"]\n    \"ServingSize\": \"Extracted Serving Size\",\n    \"Calories\": \"Extracted Calories\",\n    \"OtherInfo\": \"Any other important information extracted\"\n  }\n}\n\nRemember:\nExtract all relevant data from the label.\nThe main focus is on extracting the ingredients.\nOutput the data strictly in JSON format.",
#                         uploaded_file,
#                     ],
#                 },
#             ]
#         )

#         # Send a prompt (provide a minimal non-empty string)
#         response = chat_session.send_message("Please extract information from the image.")

#         # Return the JSON response from the model
#         return jsonify(response.text)
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     if not os.path.exists("uploads"):
#         os.makedirs("uploads")  # Create uploads directory if it doesn't exist
#     app.run(debug=True)
