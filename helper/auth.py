from flask import jsonify
import db.connection as db
from models.fam_group_user import User
from helper import utils

def loginHelper(req_data):
    try:
        encodePwd = utils.md5HashPy(req_data['password'])
        isValid = db.session.query(User.user_id,User.user_email,User.user_phone,User.user_name,User.fam_group_id,User.is_fam_admin).filter(User.user_email==req_data['email'],User.user_password==encodePwd).first()
        return isValid
    except Exception as err:
        print(err)
        return jsonify({'error':'error in validation. please contact support'}),200
    finally:
        db.close_db_con()