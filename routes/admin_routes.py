from __main__ import app
from flask import render_template

from controllers.admin import authController, categoryItemController
from controllers.admin.authController import admin_token_decode


@app.route('/admin/login', methods=['POST'])
def adminLogin():
    return authController.login()

@app.route('/admin/default-items',methods=['POST'])
def getAdminDefaultData():
    return categoryItemController.getDefaultItems()

@app.route('/admin/add-category',methods=['POST'])
def addCategory():
    return categoryItemController.addCategory()

@app.route('/admin/update-category',methods=['POST'])
def updateCategory():
    return categoryItemController.updateCategory()

@app.route('/admin/add-items',methods=['POST'])
def addItems():
    return categoryItemController.addItems()

@app.route('/admin/update-item',methods=['POST'])
def updateItems():
    return categoryItemController.updateItems()













@app.route('/admin')
def adminPage():
    return render_template('admin/index.html')

@app.route('/admin/all-items')
def allItems():
    return render_template('admin/allItems.html')

