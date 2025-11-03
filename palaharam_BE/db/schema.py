from pydantic import BaseModel
from typing import Optional

class UserDetails(BaseModel):
    firstName :str
    lastName :str 
    address :str
    mobileNumber: int
    email :str  
    password :str
    state :str
    zipCode :str

class OrderDetails(BaseModel):
    userId :int
    email: str
    OrderDetails :str
    deliveryMode: str
    totalAmount :int