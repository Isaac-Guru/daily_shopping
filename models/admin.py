from flask import jsonify
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import db.connection as db
import datetime

Base = declarative_base()

class Admin(Base):
    __tablename__ = 'ds_admin'
    admin_id = Column('admin_id', Integer, primary_key=True,autoincrement=True)
    admin_email = Column('admin_email', String)
    admin_password = Column('admin_password', String)
    admin_name = Column('admin_name', String)
    super_admin = Column('super_admin', Integer)
    created_on = Column('created_on', DateTime, default=datetime.datetime.now().timestamp())
    updated_on = Column('updated_on', DateTime)
    created_by = Column('created_by', Integer)
    updated_by = Column('updated_by', Integer)