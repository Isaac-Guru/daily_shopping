from flask import request, jsonify
import db.connection as db
from helper.admin import auth
import os
from dotenv import load_dotenv
import jwt
from functools import wraps

load_dotenv()

def admin_token_decode(f):
    @wraps(f)
    def admin_token_decode(*args, **kwargs):
        SECRET_KEY = os.getenv('ADMIN_SECRET_KEY')
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

    return admin_token_decode


def login():
    try:
        req_data = request.get_json()
        validUserRes = auth.loginHelper(req_data)
        if validUserRes:
            payload = {}
            payload['admin_id'] = validUserRes['admin_id']
            payload['admin_name'] = validUserRes['admin_name']
            payload['admin_email'] = validUserRes['admin_email']
            payload['super_admin'] = validUserRes['super_admin']
            SECRET_KEY = os.getenv('ADMIN_SECRET_KEY')
            access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify(admin_token=access_token), 200
        else:
            return jsonify({'error':'Un Authorized Access'}), 401

    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'Token not generatedaaaa. please contact support'})