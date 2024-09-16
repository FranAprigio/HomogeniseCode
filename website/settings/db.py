from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import psycopg2
import os

db = SQLAlchemy()

def database_init(app):
    with app.app_context():

        engine = db.engine
        with engine.connect() as connection:
            query = text("CREATE SCHEMA IF NOT EXISTS app")
            connection.execute(query)
            connection.commit()
        
        # Cria as tabelas
        from ..models import Base
        Base.metadata.create_all(engine)

# def get_engine():

#     config = get_dbconfig()      
#     url = URL.create(
#         drivername="postgresql",
#         username=config['pguser'],
#         password=config['pgpasswd'],
#         host=config['pghost'],
#         port=config['pgport'],
#         database=config['pgdb']
#     )
    
#     con = psycopg2.connect(
#         dbname='postgres', 
#         user=config['pguser'], 
#         host=config['pghost'], 
#         password=config['pgpasswd'],
#         port=config['pgport']
#     )
    
#     con = psycopg2.connect(dbname='postgres', user=config.get('database', 'pguser'), host=config.get('database', 'pghost'), password=config.get('database', 'pgpasswd'))     
    
#     con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

#     cur = con.cursor()

#     cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '"+config.get('database', 'pgdb')+"'")
#     exists = cur.fetchone()
#     if not exists: 
#         set_scriptdb(cur)
#         print('Created Database!')
#     else:
#         cur = get_cursor()
#         cqads = [0]  
#         cqads_item = 0          
#         cur.execute("SELECT count(0) FROM app.cqads")    
#         cqads = cur.fetchall()
#         cqads_item = [cqads_items[0] for cqads_items in cqads]

#         if int(cqads_item[0]) == 0:
#             cur.execute("INSERT INTO app.cqads(cqads_id, cqads_name, code_export_type_file) VALUES (nextval('app.cqads_cqads_id_seq'), 'Atlas-Ti', 'XLS')")
#             cur.execute("INSERT INTO app.cqads(cqads_id, cqads_name, code_export_type_file) VALUES (nextval('app.cqads_cqads_id_seq'), 'MaxQDA', 'CSV')")
#             cur.execute("INSERT INTO app.cqads(cqads_id, cqads_name, code_export_type_file) VALUES (nextval('app.cqads_cqads_id_seq'), 'NVIVO', 'XLS')")
#             cur.execute("INSERT INTO app.cqads(cqads_id, cqads_name, code_export_type_file) VALUES (nextval('app.cqads_cqads_id_seq'), 'Taguette', 'CSV')")
            
#         cur.close
    
#     engine = create_engine(url)
#     return engine

# def get_dbsession():
    
#     engine = get_engine()
    
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     return session

# def set_scriptdb(cur):

#     config = get_dbconfig()

#     cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(config.get('database', 'pgdb'))))

#     con = psycopg2.connect(dbname=config.get('database', 'pgdb'), user=config.get('database', 'pguser'), host=config.get('database', 'pghost'), password=config.get('database', 'pgpasswd'))         
#     con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     curschema = con.cursor()

#     curschema.execute(sql.SQL("CREATE SCHEMA app"))
    
def get_cursor():
    db_uri = db.engine.url

    parsed_uri = urlparse(str(db_uri))
    
    config = {
        'pguser': parsed_uri.username,
        'pgpasswd': parsed_uri.password,
        'pghost': parsed_uri.hostname,
        'pgport': parsed_uri.port,
        'pgdb': parsed_uri.path[1:]  
    }

  
    con = psycopg2.connect(
        dbname=config['pgdb'], 
        user=config['pguser'], 
        host=config['pghost'], 
        password=config['pgpasswd'],
        port=config['pgport']
    )
    
    # con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return con.cursor()

def set_audit_log():

    cur=get_cursor()

    cur.execute("SELECT 1 FROM information_schema.triggers")
    exists = cur.fetchone()
    if not exists: 

        # Open and read the SQL file
        with open(os.path.dirname(os.path.abspath('trigger_function.sql'))+'/website/settings/trigger_function.sql', 'r') as file:
            sql_queries = file.read()

        # Split the SQL file content into individual queries
        #queries = sql_queries.split(';')
        queries = sql_queries
        cur.execute(queries)   

        # Iterate over the queries and execute them
        #for query in queries:
        #    try:
        #        if query.strip() != '':
        #            cur.execute(query)
        #            cur.commit()
        #            print("Query executed successfully!")
        #    except Exception as e:
        #        print("Error executing query:", str(e))

        # Close the cursor and the database connection 

        # Open and read the SQL file
        with open(os.path.dirname(os.path.abspath('trigger_table.sql'))+'/website/settings/trigger_table.sql', 'r') as file:
            sql_queries = file.read()        
        cur.execute(sql_queries) 

    cur.close

# class InvalidOS(Exception):
#     def __init__(self, message) -> None:
#         super().__init__(message)