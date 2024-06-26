from flask import jsonify
import db.connection as db
from models.admin import Admin
from helper import utils

def loginHelper(req_data):
    try:
        encodePwd = utils.md5HashPy(req_data['password'])
        isValid = db.session.query(Admin.admin_id,Admin.admin_email,Admin.admin_name,Admin.super_admin).filter(Admin.admin_email==req_data['email'],Admin.admin_password==encodePwd).first()
        return isValid
    except Exception as err:
        print(err)
        return jsonify({'error':'Invalid Access'}),200
    finally:
        db.close_db_con()