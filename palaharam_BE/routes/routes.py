from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
import json
import base64
from db import models, schema, database
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleAuthRequest
from googleapiclient.discovery import build

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

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "token.json")

def gmail_service():
    if not os.path.exists(TOKEN_FILE):
        raise RuntimeError(
            "token.json not found — run gmail_auth_setup.py locally once to authorize this app."
        )
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, GMAIL_SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(GoogleAuthRequest())
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

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
        gmailServive = gmail_service()
        message = EmailMessage()
        message.set_content(f"Dear {data.First_Name},\n\nThank you for your order! We have received your order and it is being processed. Your order details are as follows:\n\nOrder Details: {data.order_Details}\nTotal Amount: {data.Total_Amount}\n\nWe will notify you once your order is ready for delivery.\n\nThank you for choosing our service!\n\nBest regards,\nPalaharam Team")
        message['To'] = data.Email
        message['From'] = "anushkadevg@gmail.com"
        message['Subject'] = "Order Confirmation - Palaharam"
        encoded_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')}
        send_email = gmailServive.users().messages().send(userId="me", body=encoded_message).execute()
        if send_email:
            return {"message": "Order placed successfully", "id": send_email["id"]}
        else:
            return {"issue with email sending"}
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

@router.get("/menu")
def get_menu(db: Session = Depends(get_db)):
    try:
        getMenuData = db.execute(text('SELECT * FROM Menu')).fetchall()
        menuList =[]
        for menu in getMenuData:
            menuList.append({
                "id": menu.id,
                "name": menu.name,
                "description": menu.description,
                "price": menu.price,
                "category": menu.category,
                "image_url": menu.image_url
            })
        if not menuList:
            return {"message": "No menu items found"}
        return menuList
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch menu data", "detail": str(e)})

