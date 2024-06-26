from flask import jsonify
import db.connection as db
from models.cart_assignee_map import CartAssigneeMap
from datetime import datetime



def addAssigneeHelper(req_data):
    try:
        addAssignee = CartAssigneeMap(
            cart_id=req_data['cart_id'],
            fam_group_id=req_data['fam_group_id'],
            assignee_by=req_data['user_id'],
            assigned_to=req_data['assigned_to']
            )
        db.session.add(addAssignee)
        db.session.commit()
        return True
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()

def removeAssigneeHelper(req_data):
    try:
        removeAssignee = db.session.query(CartAssigneeMap).filter(CartAssigneeMap.cart_id==req_data['cart_id'],CartAssigneeMap.fam_group_id==req_data['fam_group_id'], CartAssigneeMap.assigned_to==req_data['assigned_to']).delete()
        db.session.commit()
        if removeAssignee:
            return removeAssignee
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()

def cartAssigneeHelper(req_data):
    try:
        getAssignees = db.session.query(CartAssigneeMap.assigned_to).filter(CartAssigneeMap.cart_id==req_data['cart_id'],CartAssigneeMap.fam_group_id==req_data['fam_group_id']).all()
        db.session.commit()
        if getAssignees:
            return getAssignees
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()