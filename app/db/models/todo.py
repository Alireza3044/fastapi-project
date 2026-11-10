from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("auth_user.id"))
