from flask import request, jsonify
import db.connection as db
from helper import auth
import os
from dotenv import load_dotenv
import jwt
from functools import wraps

load_dotenv()

# decode Bearer token
def token_decode(f):
    @wraps(f)
    def token_decode(*args, **kwargs):
        SECRET_KEY = os.getenv('SECRET_KEY')
        token = str.replace(str(request.headers.get("Authorization")), 'Bearer ', '')
        if not token:
            return jsonify({'error': 'Authentication failed'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(data, *args, **kwargs)

    return token_decode

# create token while login
def login():
    try:
        req_data = request.get_json()
        validUserRes = auth.loginHelper(req_data)
        if validUserRes:
            payload = {}
            payload['user_id'] = validUserRes['user_id']
            payload['user_name'] = validUserRes['user_name']
            payload['user_email'] = validUserRes['user_email']
            payload['user_phone'] = validUserRes['user_phone']
            payload['fam_group_id'] = validUserRes['fam_group_id']
            payload['is_fam_admin'] = validUserRes['is_fam_admin']
            SECRET_KEY = os.getenv('SECRET_KEY')
            access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify(token=access_token), 200
        else:
            return jsonify({'error':'Un Authorized Access'}), 401

    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'Token not generated. please contact support'})