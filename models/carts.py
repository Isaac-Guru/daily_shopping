from flask import jsonify
from sqlalchemy import Column, Integer, String, DateTime, Enum
import db.connection as db
import datetime

class CartList(db.Base):
    __tablename__ = 'ds_cart_list'
    cart_id = Column('cart_id', Integer, primary_key=True,autoincrement=True)
    cart_name = Column('cart_name', String)
    fam_group_id = Column('fam_group_id', Integer)
    created_by = Column('created_by', Integer)
    updated_by = Column('updated_by', Integer)
    created_on = Column('created_on', DateTime)
    updated_on = Column('updated_on', DateTime)
    is_deleted = Column('is_deleted', Integer)

    # def __init__(self, data=None):
    #     self.cart_id = data['cart_id']
    #     self.cart_name = data['cart_name']
    #     self.fam_group_id = data['fam_group_id']
    #     self.created_by = data['created_by']
    #     self.updated_by = data['updated_by']
    #     self.created_on = data['created_on']
    #     self.updated_on = data['updated_on']