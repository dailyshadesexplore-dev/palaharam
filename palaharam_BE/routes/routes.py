from fastapi import APIRouter, Depends
from pydantic import BaseModel
from google.cloud import firestore
from dotenv import load_dotenv
import os
from typing import Optional
from fastapi import FastAPI, Request
import json
from db import models, schema, database
from sqlalchemy.orm import Session

load_dotenv()
# Intialize Firestore DB
db = firestore.Client()
# create a router instance
router= APIRouter()


# Create tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)
# Start database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    order_Details: Optional[object]

@router.get("/")
def health_check():
    return {"status": "API is running"}

@router.post("/guest_address")
def add_address(data: guest_Address):
    # set the guest collection
    guest_ref = db.collection("Guest")
    doc_ref = guest_ref.add(data.model_dump())
    return {"message": "Address received", "id": doc_ref[1].id}

@router.post("/users/")
def create_user(user: schema.UserDetails, db: Session = Depends(get_db)):
    # Correct filter syntax
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_user:
        return {"message": "User with this email already exists"}
    
    db_user = models.User(
        firstName=user.firstName,
        lastName=user.lastName,
        address=user.address,
        mobileNumber=user.mobileNumber,
        email=user.email,
        password=user.password,
        state=user.state,
        zipCode=user.zipCode
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/orders/")
def create_order(order:schema.OrderDetails, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == order.email).first()
    if not user:
        return "User not found"
    db_order = models.Order(
        userId=user.id,
        delivery_mode=order.deliveryMode,
        order_details=order.OrderDetails,
        total_amount=order.totalAmount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.post("/PickUp_Orders")
async def pickup_orders(request: Request):
        try:
            body = await request.json()
            order_ref = db.collection("PickUp_Orders")
            doc_ref = order_ref.add(body)
            return {"message": "Order received", "id": doc_ref[0].id}
        except Exception as e:
            return {"error": str(e)}