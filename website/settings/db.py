import os
import psycopg2
import platform


from psycopg2 import sql
from configparser import ConfigParser
from sqlalchemy.orm import sessionmaker
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

def get_OS():
    return platform.system()

def get_dbconfig():
    OS = get_OS()
    config = ConfigParser()  
    match OS:
        case 'Linux':
            
            config.read(os.path.dirname(os.path.abspath('conf.ini'))+'/website/settings/conf.ini')
        case 'Windows':
            
            config.read(os.path.dirname(os.path.abspath('conf.ini'))+'\\website\\settings\\conf.ini')
        case "Darwin":
            raise InvalidOS("Mac OS Is not Acceptable")
        case _:
            raise InvalidOS("Unknow OS")
    
    return config

def get_engine():

    config = get_dbconfig()      
    url = URL.create(
        drivername="postgresql",
        username=config.get('database', 'pguser'),
        password=config.get('database', 'pgpasswd'),
        host=config.get('database', 'pghost'),
        database=config.get('database', 'pgdb')
    )
    
    con = psycopg2.connect(dbname='postgres', user=config.get('database', 'pguser'), host=config.get('database', 'pghost'), password=config.get('database', 'pgpasswd'))     
    
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = con.cursor()

    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '"+config.get('database', 'pgdb')+"'")
    exists = cur.fetchone()
    if not exists: 
        set_scriptdb(cur)
        print('Created Database!')

    
    engine = create_engine(url)
    return engine

def get_dbsession():
    
    engine = get_engine()
    
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def set_scriptdb(cur):

    config = get_dbconfig()

    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(config.get('database', 'pgdb'))))

    con = psycopg2.connect(dbname=config.get('database', 'pgdb'), user=config.get('database', 'pguser'), host=config.get('database', 'pghost'), password=config.get('database', 'pgpasswd'))         
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    curschema = con.cursor()

    curschema.execute(sql.SQL("CREATE SCHEMA app"))
    
def get_cursor():
    config = get_dbconfig()
    con = psycopg2.connect(dbname=config.get('database', 'pgdb'), user=config.get('database', 'pguser'), host=config.get('database', 'pghost'), password=config.get('database', 'pgpasswd'))         
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return con.cursor()


class InvalidOS(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)