from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # ✅ Primary Key
    firstName = Column(String)
    lastName = Column(String) 
    address = Column(String) 
    mobileNumber = Column(Integer, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    state = Column(String)
    zipCode = Column(String)
    created_at = Column(DateTime, default=datetime.now())

    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # ✅ Primary Key
    userId = Column(Integer, ForeignKey("users.id"))
    order_details = Column(String)  
    delivery_mode = Column(String)
    total_amount = Column(Integer)
    order_date = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="orders")