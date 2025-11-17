from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
import json
from db import models, schema, database
from sqlalchemy.orm import Session

load_dotenv()
# Intialize Firestore DB
# db = firestore.Client()
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
def add_address(data: schema.guest_Address, db: Session = Depends(get_db)):
    try:
        mobile_val = None
        if getattr(data, 'Mobile_Number', None) not in (None, ""):
            try:
                mobile_val = int(data.Mobile_Number)
            except Exception:
                mobile_val = None

        order_details_json = None
        if getattr(data, 'order_Details', None) is not None:
            try:
                order_details_json = json.dumps(data.order_Details)
            except Exception:
                order_details_json = None

        db_guest = models.Guest(
            firstName=data.First_Name,
            lastName=data.Last_Name,
            address=data.Address_Line,
            mobileNumber=mobile_val,
            email=data.Email,
            state=data.State,
            zipCode=data.Zip_Code,
            orderDetails=order_details_json,
            deliveryMode=data.Delivery_Mode,
            Payment_Mode=data.Payment_Mode,
            totalAmount=getattr(data, 'Total_Amount', None)
        )
        db.add(db_guest)
        db.commit()
        db.refresh(db_guest)
        return {"message": "Order placed successfully", "id": db_guest.id}
    except Exception as e:
        # Raise HTTPException so client receives 400 with details
        raise HTTPException(status_code=400, detail={"error": "Failed to create guest record", "detail": str(e)})

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
        # Firestore client `db` may not be configured in this repo (commented out above).
        db_client = globals().get('db')
        if db_client and hasattr(db_client, 'collection'):
            order_ref = db_client.collection("PickUp_Orders")
            doc_ref = order_ref.add(body)
            return {"message": "Order received", "id": doc_ref[0].id}
        # Firestore not configured — return the payload for debugging instead
        return {"message": "Firestore not configured on server", "received": body}
    except Exception as e:
        return {"error": str(e)}