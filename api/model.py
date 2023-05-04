
from sqlalchemy import create_engine, Column, Integer, String,Date,Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False,unique=True)
    details = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    date = Column(Date)

