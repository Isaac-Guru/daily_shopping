from flask import request, jsonify
import db.connection as db
from helper import user
from controllers.authController import token_decode

# get all family users
@token_decode
def getFamUsers(decoded_token):
    try:
        req_data = {"fam_group_id":decoded_token['fam_group_id']}
        famUsers = user.getMyFamUsers(req_data)
        fam_user_list = []
        if famUsers:
            for user_detail in famUsers:
                tempData = {}
                tempData['user_id'] = user_detail['user_id']
                tempData['user_name'] = user_detail['user_name']
                tempData['user_phone'] = user_detail['user_phone']
                fam_user_list.append(tempData)
        return jsonify({'error':'','fam_users':fam_user_list}),200
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})
