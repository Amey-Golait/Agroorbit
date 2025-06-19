from pydantic import BaseModel
from typing import Optional, List
from fastapi import Form


class StaffCreate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    manager_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        city: Optional[str] = Form(None),
        manager_name: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        role: Optional[str] = Form(None),
    ):
        return cls(
            name=name,
            email=email,
            phone=phone,
            city=city,
            manager_name=manager_name,
            password=password,
            role=role,
        )

class StaffUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    manager_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        city: Optional[str] = Form(None),
        manager_name: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        role: Optional[str] = Form(None),
    ):
        return cls(
            name=name,
            email=email,
            phone=phone,
            city=city,
            manager_name=manager_name,
            password=password,
            role=role,
        )

class StaffOut(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    city: Optional[str]
    manager_name: Optional[str]
    role: Optional[str]

    class Config:
        from_attributes = True

def as_form(
        staff_id: List[int] = Form(...),
):
    return staff_id