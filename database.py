from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from decouple import config
from typing import TypeAlias, Annotated

db_name = config("DB_NAME")
db_user = config("DB_USER")
db_password = config("DB_PASSWORD")
db_host = config("DB_HOST")
db_port = config("DB_PORT", cast=int)

url = "postgresql+psycopg2://%s:%s@%s:%s/%s?client_encoding=utf8" % (db_user, db_password, db_host, db_port, db_name)

engine = create_engine(url)

SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DB_DEP: TypeAlias = Annotated[Session, Depends(get_db)]
