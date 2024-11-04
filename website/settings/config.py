import os
import configparser

PG = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "user": os.getenv("POSTGRES_USER"),
    "passwd": os.getenv("POSTGRES_PASSWORD"),
    "db": os.getenv("POSTGRES_DB"),
}

print(PG)

class AttrDict(dict):
    def __init__(self,*args, **kwargs):
        super(AttrDict,self).__init__(*args,**kwargs)
        self.__dict__ = self

def check_ini_config_exists():
    if os.path.exists('./website/settings/conf.ini'):
        return True
    else:
        return False

def create_ini_config(dbhost:str,dbport:str,dbuser:str,dbpassword:str,db:str):
    config = configparser.ConfigParser()
    config.add_section("Database")
    config.set('Database','Host',dbhost)
    config.set('Database','Port',dbport)
    config.set('Database','User',dbuser)
    config.set('Database','Password',dbpassword)
    config.set('Database','Database',db)
    with open('./website/settings/conf.ini','w') as file:
        config.write(file)

def get_ini_config():
    config = configparser.ConfigParser(dict_type=AttrDict)
    config.read('./website/settings/conf.ini')
    data = AttrDict(config._sections)
    return data
create_ini_config(str(None),"666","Jones","69696","Hell")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{PG['user']}:{PG['passwd']}@{PG['host']}:{PG['port']}/{PG['db']}"
)