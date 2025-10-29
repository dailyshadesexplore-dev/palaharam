from fastapi import APIRouter
from pydantic import BaseModel
from google.cloud import firestore
from dotenv import load_dotenv
import os
from typing import Optional
from fastapi import FastAPI, Request
import json

load_dotenv()
# Intialize Firestore DB
db = firestore.Client()
# create a router instance
router= APIRouter()

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

@router.post("/PickUp_Orders")
async def pickup_orders(request: Request):
        try:
            body = await request.json()
            order_ref = db.collection("PickUp_Orders")
            doc_ref = order_ref.add(body)
            return {"message": "Order received", "id": doc_ref[0].id}
        except Exception as e:
            return {"error": str(e)}