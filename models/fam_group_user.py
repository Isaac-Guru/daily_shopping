from flask import jsonify
from sqlalchemy import Column, Integer, String, DateTime, Enum
import db.connection as db
import datetime

class User(db.Base):
    __tablename__ = 'ds_family_group_user'
    user_id = Column('user_id', Integer, primary_key=True, autoincrement=True)
    user_name = Column('user_name', String)
    user_email = Column('user_email', String)
    user_password = Column('user_password', String)
    user_phone = Column('user_phone', String)
    is_fam_admin = Column('is_fam_admin', Integer)
    fam_group_id = Column('fam_group_id', Integer)
    created_on = Column('created_on', DateTime, default=datetime.datetime.now().timestamp())
    updated_on = Column('updated_on', DateTime, default=datetime.datetime.now().timestamp())
