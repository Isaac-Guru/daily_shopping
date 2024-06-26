from flask import jsonify
import db.connection as db
from models.categories import AllCategories
from models.category_item import CategoryItem
from models.carts import CartList
from models.cart_details import CartListDetails
from models.cart_assignee_map import CartAssigneeMap
from datetime import datetime
from sqlalchemy import not_, or_
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.sql import func
# from sqlalchemy.dialects.mysql import JSON

def myCartsHelper(req_data):
    try:
        myCarts = db.session.query(CartList.cart_id,CartList.cart_name, CartListDetails.item_json,CartList.created_on).join(CartListDetails, CartList.cart_id==CartListDetails.cart_id).filter(CartList.created_by==req_data['user_id'],CartList.fam_group_id==req_data['fam_group_id'],or_(CartList.is_deleted!=True,CartList.is_deleted.is_(None))).order_by(CartList.cart_id.desc()).limit(100).all()
        if myCarts:
            return myCarts
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()

def assignedCartsHelper(req_data):
    try:
        assignedCarts = db.session.query(CartList.cart_id,CartList.cart_name, CartListDetails.item_json,CartList.created_on).join(CartListDetails, CartList.cart_id==CartListDetails.cart_id).join(CartAssigneeMap, CartList.cart_id==CartAssigneeMap.cart_id).filter(CartAssigneeMap.assigned_to==req_data['user_id'],CartList.fam_group_id==req_data['fam_group_id']).group_by(CartAssigneeMap.cart_id).order_by(CartList.cart_id.desc()).all()
        if assignedCarts:
            return assignedCarts
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()

def getCartHelper(req_data):
    try:
        cartData = db.session.query(CartList.cart_id,CartList.cart_name, CartListDetails.item_json,CartList.created_on).join(CartListDetails, CartList.cart_id==CartListDetails.cart_id).filter(CartList.cart_id==req_data['cart_id'],CartList.fam_group_id==req_data['fam_group_id']).first()
        if cartData:
            return cartData
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()

def updateCartHelper(req_data):
    try:
        updateCartDetail = db.session.query(CartListDetails).filter(CartListDetails.cart_id==req_data['cart_id']).update({'item_json':req_data['item_json'],'updated_by':req_data['user_id']})
        db.session.commit()
        if updateCartDetail:
            updateCart = db.session.query(CartList).filter(CartList.cart_id==req_data['cart_id'],CartList.fam_group_id==req_data['fam_group_id']).update({'cart_name':req_data['cart_name'],'updated_by':req_data['user_id']})
            db.session.commit()
            if updateCart:
                return True
            return False
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()

def updatePurchasedHelper(req_data):
    try:
        updatePuchase = db.session.query(CartListDetails).filter(CartListDetails.cart_id==req_data['cart_id']).update({'item_json':req_data['item_json']})
        db.session.commit()
        if updatePuchase:
            return True
        return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()

def delCartHelper(req_data):
    try:
        db.session.query(CartAssigneeMap).filter(CartAssigneeMap.cart_id == req_data['cart_id']).delete()
        db.session.flush()
            
        delCart = db.session.query(CartList).filter(CartList.cart_id==req_data['cart_id'],CartList.created_by==req_data['user_id'],CartList.fam_group_id==req_data['fam_group_id']).update({'is_deleted':True})
        db.session.commit()
        if delCart:
            return True
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()

def addCartHelper(req_data):
    try:
        addCart = CartList(
            cart_name=req_data['cart_name'],
            fam_group_id=req_data['fam_group_id'],
            created_by=req_data['user_id'],
            created_on=datetime.now()
            )
        db.session.add(addCart)
        db.session.commit()
        cart_id = addCart.cart_id
        if cart_id:
            print(cart_id)
        else:
            return False
        
        addCartDetail = CartListDetails(
            cart_id=cart_id,
            item_json=req_data['item_json'],
            created_by=req_data['user_id'],
            created_on=datetime.now()
            )
        db.session.add(addCartDetail)
        db.session.commit()
        return True
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()

def getAllCategoriesHelper():
    try:
        getAllCat = db.session.query(AllCategories.category_id,AllCategories.category_name, AllCategories.category_name_alias).order_by(AllCategories.category_id.asc()).all()
        
        if getAllCat:
            return getAllCat
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()

def getAllCatItemHelper():
    try:
        getAllCat = db.session.query(CategoryItem.category_id,CategoryItem.item_id,CategoryItem.item_name, CategoryItem.item_name_alias).order_by(CategoryItem.item_id.asc()).all()
        
        if getAllCat:
            return getAllCat
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()