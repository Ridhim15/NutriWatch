from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response, send_from_directory

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


