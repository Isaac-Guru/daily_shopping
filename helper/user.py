from flask import jsonify
import db.connection as db
from models.fam_group_user import User
from datetime import datetime

def getMyFamUsers(req_data):
    try:
        myfamGrpUsers = db.session.query(User.user_id,User.user_name,User.user_phone).filter(User.fam_group_id==req_data['fam_group_id'])
        if myfamGrpUsers:
            return myfamGrpUsers
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()
    