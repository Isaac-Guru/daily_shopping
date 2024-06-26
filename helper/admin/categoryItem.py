from flask import jsonify
import db.connection as db
from models.categories import AllCategories
from models.category_item import CategoryItem
from datetime import datetime
from sqlalchemy import not_, or_




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

def addCategoryHelper(req_data):
    try:
        addCat = AllCategories(
            category_name=req_data['category_name'],
            category_name_alias=req_data['category_name_alias'],
            created_by_admin=True,
            created_on=datetime.now()
            )
        db.session.add(addCat)
        db.session.commit()
        if addCat:
            return True
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()


def updateCategoryHelper(req_data):
    try:
        updateCat = db.session.query(AllCategories).filter(AllCategories.category_id==req_data['category_id']).update({'category_name':req_data['category_name'],'category_name_alias':req_data['category_name_alias']})
        db.session.commit()
        if updateCat:
            return True
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()

def addItemsHelper(inser_data):
    try:
        db.session.bulk_insert_mappings(CategoryItem,inser_data)
        db.session.commit()
        return True
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()


def updateItemsHelper(req_data):
    try:
        updateItems = db.session.query(CategoryItem).filter(CategoryItem.item_id==req_data['item_id']).update({'item_name':req_data['item_name'],'item_name_alias':req_data['item_name_alias']})
        db.session.commit()
        if updateItems:
            return True
        else:
            return False
    except Exception as err:
        print(err)
        return False
    finally:
        db.close_db_con()