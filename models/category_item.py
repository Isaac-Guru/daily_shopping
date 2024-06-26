from flask import jsonify
from sqlalchemy import Column, Integer, String, DateTime, Enum
import db.connection as database
import datetime

class CategoryItem(database.Base):
    __tablename__ = 'ds_category_item'
    __table_args__ = {'autoload': True}
    item_id = Column('item_id', Integer, primary_key=True, autoincrement=True)
    item_name = Column('item_name', String)
    item_name_alias = Column('item_name_alias', String)
    created_on = Column('created_on', DateTime, default=datetime.datetime.now().timestamp())
    updated_on = Column('updated_on', DateTime)
    created_by = Column('created_by', Integer)
    created_by_admin = Column('created_by_admin', Integer)
