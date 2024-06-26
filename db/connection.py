import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
import traceback
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

mysql_connection_string = os.getenv('MYSQL_CON_STR')

pymysql.install_as_MySQLdb()


try:
    Engine = sa.create_engine(mysql_connection_string, poolclass=NullPool)
    Connection = Engine.connect()

    Base = declarative_base()

    # reflect current database engine to metadata
    # Metadata = sa.MetaData(Engine)
    Base.metadata.bind = Engine
    # metadata.reflect()

    # Session = sa.orm.sessionmaker(bind=Engine)()
    session = sa.orm.sessionmaker(bind=Engine, expire_on_commit=False)()

except Exception as err:
    print(traceback.format_exc())
    raise Exception("Error: " + str(err))


def close_db_con():
    session.close()
    Connection.close()
    Engine.dispose()
