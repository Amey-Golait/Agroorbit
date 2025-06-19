from pydantic import BaseModel
from fastapi import Form
from typing import Optional, List
from datetime import date

class CustomerBase(BaseModel):
    name: Optional[str]
    firm_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    pan_no: Optional[str]
    user_type: Optional[str]
    address: Optional[str]
    licence_no: Optional[int]
    licence_expiry_date: Optional[date]
    password: Optional[str]

class CustomerCreate(CustomerBase):
    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(None),
        firm_name: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        pan_no: Optional[str] = Form(None),
        user_type: Optional[str] = Form(None),
        address: Optional[str] = Form(None),
        licence_no: Optional[int] = Form(None),
        licence_expiry_date: Optional[date] = Form(None),
        password: Optional[str] = Form(None),
    ):
        return cls(
            name=name,
            firm_name=firm_name,
            phone=phone,
            email=email,
            pan_no=pan_no,
            user_type=user_type,
            address=address,
            licence_no=licence_no,
            licence_expiry_date=licence_expiry_date,
            password=password,
        )

class CustomerUpdate(CustomerBase):
    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(None),
        firm_name: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        pan_no: Optional[str] = Form(None),
        user_type: Optional[str] = Form(None),
        address: Optional[str] = Form(None),
        licence_no: Optional[int] = Form(None),
        licence_expiry_date: Optional[date] = Form(None),
        password: Optional[str] = Form(None),
    ):
        return cls(
            name=name,
            firm_name=firm_name,
            phone=phone,
            email=email,
            pan_no=pan_no,
            user_type=user_type,
            address=address,
            licence_no=licence_no,
            licence_expiry_date=licence_expiry_date,
            password=password,
        )

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True

def as_form(
        customer_id: List[int] = Form(...),
):
    return customer_id