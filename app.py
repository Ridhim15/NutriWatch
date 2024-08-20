from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response, send_from_directory
from flask_restful import Api, Resource
from flask_session import Session
from flask_dance.contrib.google import make_google_blueprint, google
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from requests.models import Response
from dotenv import load_dotenv
from os import environ
from datetime import datetime
import json

load_dotenv()

# -------------------- Main App --------------------
app = Flask(__name__)
api = Api(app)

# ------------------------------------------------------------------------------------------------
# ---------------------------------------- ROUTES / VIEWS ----------------------------------------
# ------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')
