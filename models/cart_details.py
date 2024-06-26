from flask import jsonify
from sqlalchemy import Column, Integer, String, DateTime, Enum, JSON
import db.connection as db
import datetime

class CartListDetails(db.Base):
    __tablename__ = 'ds_cart_list_details'
    cart_list_id = Column('cart_list_id', Integer, primary_key=True,autoincrement=True)
    cart_id = Column('cart_id', Integer)
    item_json = Column('item_json', JSON)
    created_by = Column('created_by', Integer)
    updated_by = Column('updated_by', Integer)
    created_on = Column('created_on', DateTime)
    updated_on = Column('updated_on', DateTime)

    # def __init__(self, data=None):
    #     self.cart_list_id = data['cart_list_id']
    #     self.cart_id = data['cart_id']
    #     self.item_json = data['item_json']
    #     self.created_by = data['created_by']
    #     self.updated_by = data['updated_by']
    #     self.created_on = data['created_on']
    #     self.updated_on = data['updated_on']