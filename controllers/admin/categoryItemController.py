from flask import request, jsonify
import db.connection as db
from helper.admin import categoryItem
from controllers.admin.authController import admin_token_decode

@admin_token_decode
def getDefaultItems(admin_token_decode):
    try:
        allCat = categoryItem.getAllCategoriesHelper()
        allCatData = {}
        if allCat:
            for x in allCat:
                tempData = {}
                tempData['category_id'] = x['category_id']
                tempData['category_name'] = x['category_name']
                tempData['category_name_alias'] = x['category_name_alias']
                key = x["category_id"]
                allCatData[key] = tempData

        allItem = categoryItem.getAllCatItemHelper()
        allItemData = {}
        if allItem:
            for x in allItem:
                tempData = {}
                tempData['category_id'] = x['category_id']
                tempData['item_id'] = x['item_id']
                tempData['item_name'] = x['item_name']
                tempData['item_name_alias'] = x['item_name_alias']
                key = x["category_id"]
                if(key in allItemData):
                    allItemData[key].append(tempData)
                else:
                    allItemData[key] = []
                    allItemData[key].append(tempData)
        return jsonify({'error':'','all_categories':allCatData,'all_categories_item':allItemData}),200
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

@admin_token_decode
def addCategory(admin_token_decode):
    req_data = request.get_json()
    try:
        addCategoryRes = categoryItem.addCategoryHelper(req_data)
        if addCategoryRes:
            return jsonify({'error':''})
        else:
            return jsonify({'status':200, 'error':'something went wrong. please contact support'})
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

@admin_token_decode
def updateCategory(admin_token_decode):
    req_data = request.get_json()
    try:
        updateCategoryRes = categoryItem.updateCategoryHelper(req_data)
        if updateCategoryRes:
            return jsonify({'error':''})
        else:
            return jsonify({'status':200, 'error':'something went wrong. please contact support'})
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

@admin_token_decode
def addItems(admin_token_decode):
    req_data = request.get_json()
    try:
        addaddItemsRes = categoryItem.addItemsHelper(req_data)
        if addaddItemsRes:
            return jsonify({'error':''})
        else:
            return jsonify({'status':200, 'error':'something went wrong. please contact support'})
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

@admin_token_decode
def updateItems(admin_token_decode):
    req_data = request.get_json()
    try:
        updateItemsRes = categoryItem.updateItemsHelper(req_data)
        if updateItemsRes:
            return jsonify({'error':''})
        else:
            return jsonify({'status':200, 'error':'something went wrong. please contact support'})
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})