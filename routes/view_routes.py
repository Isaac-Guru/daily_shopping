from __main__ import app
from flask import render_template

@app.route('/my-carts')
def my_carts():
    return render_template('all_carts.html')

@app.route('/view-cart')
def view_cart():
    return render_template('view_cart.html')

@app.route('/add-new-cart')
def addNewCart():
    return render_template('add_cart.html')

@app.route('/edit-cart')
def editCart():
    return render_template('edit_cart.html')