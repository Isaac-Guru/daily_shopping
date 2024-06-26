from flask import request, jsonify
import db.connection as db
from models.categories import AllCategories
from helper import carts
from helper import assignee
from controllers.authController import token_decode


def getAllCategories():
    try:
        categories = db.session.query(AllCategories.category_id, AllCategories.category_name).all()
        all_categories = []
        for x in categories:
            tempData = {}
            tempData['category_id'] = x['category_id']
            tempData['category_name'] = x['category_name']
            all_categories.append(tempData)
        return jsonify({'data':all_categories}),200
    except Exception as err:
        print(err)
        return jsonify({'error':'some issue'}),200
    finally:
        db.close_db_con()

# get carts created by myself
@token_decode
def getMyCarts(decoded_token):
    try:
        # req_data = request.get_json()
        req_data = {"user_id":decoded_token['user_id'],"fam_group_id":decoded_token['fam_group_id']}
        mycarts = carts.myCartsHelper(req_data)
        my_cart_list = []
        if mycarts:
            for x in mycarts:
                tempData = {}
                tempData['cart_id'] = x['cart_id']
                tempData['cart_name'] = x['cart_name']
                tempData['item_json'] = x['item_json']
                tempData['created_date'] = x['created_on'].strftime("%d-%b-%Y %I.%M %p")
                my_cart_list.append(tempData)
        assignedCarts = carts.assignedCartsHelper(req_data)
        assigned_cart_list = []
        if assignedCarts:
            for x in assignedCarts:
                tempData = {}
                tempData['cart_id'] = x['cart_id']
                tempData['cart_name'] = x['cart_name']
                tempData['item_json'] = x['item_json']
                tempData['created_date'] = x['created_on'].strftime("%d-%b-%Y %I.%M %p")
                assigned_cart_list.append(tempData)
        return jsonify({'error':'','my_cart_list':my_cart_list,'assigned_cart_list':assigned_cart_list}),200
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

# get cart by id
@token_decode
def getCart(decoded_token):
    try:
        req_data = request.get_json()
        input_data = {"user_id":decoded_token['user_id'],"fam_group_id":decoded_token['fam_group_id'],"cart_id":req_data['cart_id']}
        cartRes = carts.getCartHelper(input_data)
        if cartRes:
            tempData = {}
            tempData['cart_id'] = cartRes['cart_id']
            tempData['cart_name'] = cartRes['cart_name']
            tempData['item_json'] = cartRes['item_json']
            tempData['created_date'] = cartRes['created_on'].strftime("%d-%b-%Y %I.%M %p")
            return jsonify({'data':tempData}),200
        else:
            return jsonify({'error':'','status':200, 'error':'No cart found'})
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

# updated cart after purchase
@token_decode
def updatePurchasedDetail(decoded_token):
    req_data = request.get_json()
    input_data = {"cart_id":req_data['cart_id'],"item_json":req_data['item_json']}
    try:
        updateRes = carts.updatePurchasedHelper(input_data)
        if updateRes:
            return jsonify({'error':''})
        else:
            return jsonify({'status':200, 'error':'something went wrong. please contact support'})
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

# edit cart detail
@token_decode
def updateCart(decoded_token):
    req_data = request.get_json()
    input_data = {"user_id":decoded_token['user_id'],"fam_group_id":decoded_token['fam_group_id'],"cart_id":req_data['cart_id'],"cart_name":req_data['cart_name'],"item_json":req_data['item_json']}
    try:
        updateRes = carts.updateCartHelper(input_data)
        if updateRes:
            return jsonify({'error':''})
        else:
            return jsonify({'status':200, 'error':'something went wrong. please contact support'})
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

# add new cart
@token_decode
def addCart(decoded_token):
    req_data = request.get_json()
    input_data = {"user_id":decoded_token['user_id'],"fam_group_id":decoded_token['fam_group_id'],"cart_name":req_data['cart_name'],"item_json":req_data['item_json']}
    try:
        addCartRes = carts.addCartHelper(input_data)
        if addCartRes:
            return jsonify({'error':''})
        else:
            return jsonify({'status':200, 'error':'something went wrong. please contact support'})
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

# delete cart
@token_decode
def delCart(decoded_token):
    req_data = request.get_json()
    input_data = {"user_id":decoded_token['user_id'],"fam_group_id":decoded_token['fam_group_id'],"cart_id":req_data['cart_id']}
    try:
        delCartRes = carts.delCartHelper(input_data)
        if delCartRes:
            return jsonify({'error':''})
        else:
            return jsonify({'status':200, 'error':'error in del cart. please contact support'})
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

# assign the cart to the user in fam group
@token_decode
def addAssignee(decoded_token):
    try:
        req_data = request.get_json()
        input_data = {"user_id":decoded_token['user_id'],"fam_group_id":decoded_token['fam_group_id'],"cart_id":req_data['cart_id'],"assigned_to":req_data['assigned_to']}
        addAssigneeRes = assignee.addAssigneeHelper(input_data)
        if addAssigneeRes:
            return jsonify({'error':''})
        else:
            return jsonify({'status':200, 'error':'something went wrong. please contact support'})
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

# remove assigne from the cart
@token_decode
def removeAssignee(decoded_token):
    try:
        req_data = request.get_json()
        input_data = {"user_id":decoded_token['user_id'],"fam_group_id":decoded_token['fam_group_id'],"cart_id":req_data['cart_id'],"assigned_to":req_data['assigned_to']}
        removeAssigneeRes = assignee.removeAssigneeHelper(input_data)
        if removeAssigneeRes:
            return jsonify({'error':''})
        else:
            return jsonify({'status':200, 'error':'something went wrong. please contact support'})
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})

# get default items
@token_decode
def getDefaultItems(decoded_token):
    try:
        allCat = carts.getAllCategoriesHelper()
        allCatData = {}
        if allCat:
            for x in allCat:
                tempData = {}
                tempData['category_id'] = x['category_id']
                tempData['category_name'] = x['category_name']
                tempData['category_name_alias'] = x['category_name_alias']
                key = x["category_id"]
                allCatData[key] = tempData

        allItem = carts.getAllCatItemHelper()
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

# get assigness list map to the cart
@token_decode     
def cartAssignees(decoded_token):
    try:
        req_data = request.get_json()
        input_data = {"fam_group_id":decoded_token['fam_group_id'],"cart_id":req_data['cart_id']}
        assigneeRes = assignee.cartAssigneeHelper(input_data)
        assignedList = []
        if assigneeRes:
            for x in assigneeRes:
                assignedList.append(x['assigned_to'])
        return jsonify({'error':'','status':200, 'assigned_users':assignedList}),200
    except Exception as err:
        print(err)
        return jsonify({'status':200, 'error':'something went wrong. please contact support'})