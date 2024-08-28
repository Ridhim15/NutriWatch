from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response, send_from_directory
import os
from  dotenv import load_dotenv
import base64


load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/userinfo')
def form():
    return render_template('userinfo.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scanner')
def scanner():
    return render_template('scanner.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/status', methods=['GET'])
def status():
    return render_template('status.html')

@app.route('/capture', methods=['POST'])
def capture():
    # Capture image from base64 data (received from frontend)
    image_data = request.form['image']
    image_data = image_data.split(',')[1]  # Remove the base64 header
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'captured_image.png')
    
    with open(image_path, "wb") as fh:
        fh.write(base64.b64decode(image_data))
    
    return image_path
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    # app.run(debug=True,host='192.168.29.235')
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


