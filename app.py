from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response, send_from_directory
import google.generativeai as genai
import os
from  dotenv import load_dotenv
from model import extract_data
load_dotenv()
#Configure Google Generative AI
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
    generation_config=generation_config,
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/status', methods=['GET'])
def status():
    return "Server is running"

@app.route('/upload', methods=['POST'])
def upload():
    return extract_data()

if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")  # Create uploads directory if it doesn't exist
    app.run(debug=True,host='192.168.29.235')
