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

class guest_Address(BaseModel):
    Delivery_Mode: str
    Payment_Mode: str
    First_Name: str
    Last_Name: str
    Address_Line: str
    Mobile_Number: str
    Email: str
    Floor_Apt_Number: Optional[str]
    State: str
    Zip_Code: str
    order_Details: object
    Total_Amount: int