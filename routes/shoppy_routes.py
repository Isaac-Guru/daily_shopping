from __main__ import app

from controllers import shoppyController, authController, userController
from controllers.authController import token_decode
print("shoppy route")
@app.route('/login', methods=['POST'])
def userLogin():
    return authController.login()

@app.route('/get-category', methods=['GET'])
def getAllCategories():
    return shoppyController.getAllCategories()

@app.route('/get-my-carts',methods=['POST'])
def getMyCarts():
    return shoppyController.getMyCarts()

@app.route('/get-cart',methods=['POST'])
def getCart():
    return shoppyController.getCart()

@app.route('/update-cart',methods=['POST'])
def updateCart():
    return shoppyController.updateCart()

@app.route('/add-cart',methods=['POST'])
def addCart():
    return shoppyController.addCart()

@app.route('/del-cart',methods=['POST'])
def delCart():
    return shoppyController.delCart()

@app.route('/add-assignee',methods=['POST'])
def addAssignee():
    return shoppyController.addAssignee()

@app.route('/remove-assignee',methods=['POST'])
def removeCart():
    return shoppyController.removeAssignee()

@app.route('/get-default-items',methods=['POST'])
def getDefaultData():
    return shoppyController.getDefaultItems()

@app.route('/update-purchase-details',methods=['POST'])
def updatePurchasedDetail():
    return shoppyController.updatePurchasedDetail()

@app.route('/get-fam-users',methods=['POST'])
def getFamUsers():
    return userController.getFamUsers()

@app.route('/cart-assignees',methods=['POST'])
def cartAssignees():
    return shoppyController.cartAssignees()