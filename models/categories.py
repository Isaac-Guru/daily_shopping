from flask import jsonify
from sqlalchemy import Column, Integer, String, DateTime, Enum
import db.connection as database
import datetime

class AllCategories(database.Base):
    __tablename__ = 'ds_category'
    __table_args__ = {'autoload': True}
    category_id = Column('category_id', Integer, primary_key=True, autoincrement=True)
    category_name = Column('category_name', String)
    created_on = Column('created_on', DateTime, default=datetime.datetime.now().timestamp())
    updated_on = Column('updated_on', DateTime, default=datetime.datetime.now().timestamp())
    created_by_admin = Column('created_by_admin', Integer)
