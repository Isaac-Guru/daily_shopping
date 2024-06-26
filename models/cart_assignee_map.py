from flask import jsonify
from sqlalchemy import Column, Integer, String, DateTime, Enum
import db.connection as db
import datetime

class CartAssigneeMap(db.Base):
    __tablename__ = 'ds_cart_assignee_map'
    cart_assign_id = Column('cart_assign_id', Integer, primary_key=True,autoincrement=True)
    cart_id = Column('cart_id', Integer)
    fam_group_id = Column('fam_group_id', Integer)
    assignee_by = Column('assignee_by', Integer)
    assigned_to = Column('assigned_to', Integer)
    created_on = Column('created_on', DateTime, default=datetime.datetime.now().timestamp())
    updated_on = Column('updated_on', DateTime)

    # def __init__(self, data=None):
    #     self.cart_assign_id = data['cart_assign_id']
    #     self.cart_id = data['cart_id']
    #     self.fam_group_id = data['fam_group_id']
    #     self.assignee_by = data['assignee_by']
    #     self.assigned_to = data['assigned_to']
    #     self.created_on = data['created_on']
    #     self.updated_on = data['updated_on']