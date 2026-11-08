from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from decouple import config
from typing import TypeAlias, Annotated

db_name = config("DB_NAME")
db_username = config("DB_USER_NAME")
db_password = config("DB_USER_PASSWORD")

url = "postgresql+psycopg2://%s:%s@localhost:5432/%s?client_encoding=utf8" % (db_username, db_password, db_name)

engine = create_engine(url)

SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DB: TypeAlias = Annotated[Session, Depends(get_db)]
