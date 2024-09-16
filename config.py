import os

PG = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "user": os.getenv("POSTGRES_USER"),
    "passwd": os.getenv("POSTGRES_PASSWORD"),
    "db": os.getenv("POSTGRES_DB"),
}

print(PG)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{PG['user']}:{PG['passwd']}@{PG['host']}:{PG['port']}/{PG['db']}"
)