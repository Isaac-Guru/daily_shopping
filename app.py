# print("hello")
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

load_dotenv()
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Configure the application with a secret key and JWT options
app.config['JWT_SECRET_KEY'] = 'dsgshbkj@gds^66778gyad'  # just for temp
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

from routes import *

@app.route('/')
def index():
    return render_template('index.html')
    # return jsonify({"message": "Service up & running"}),200

if __name__ == '__main__':
    app.debug = True
    app.run(host=HOST, port=PORT, use_reloader=False)