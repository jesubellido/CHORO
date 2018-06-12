from sqlalchemy import Column, Integer, String
from database import connector

class User(connector.Manager.Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True)
    name= Column(String(20))
    fullname=Column(String(30))
    password=Column(String(10))