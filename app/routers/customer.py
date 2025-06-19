from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import customer as customer_schema
from app.crud import customer as customer_crud
from app.database import get_db

router = APIRouter(prefix="/customers", tags=["customers"])
templates = Jinja2Templates(directory="app/templates")

# --- UI ROUTES ---

@router.get("/ui", response_class=HTMLResponse)
def customer_ui_list(request: Request, db: Session = Depends(get_db)):
    customers = customer_crud.get_customers(db)
    return templates.TemplateResponse("customer/customer_table.html", {"request": request, "customers": customers})

# --- API ROUTES ---

@router.post("/", response_model=customer_schema.Customer)
def create_customer_api(
    name: Optional[str] = Form(None),
    firm_name: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    pan_no: Optional[str] = Form(None),
    user_type: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    licence_no: Optional[int] = Form(None),
    licence_expiry_date: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    customer_data = customer_schema.CustomerCreate(
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
    return customer_crud.create_customer(db, customer_data)

@router.put("/{customer_id}", response_model=customer_schema.Customer)
def update_customer_api(
    customer_id: int,
    name: Optional[str] = Form(None),
    firm_name: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    pan_no: Optional[str] = Form(None),
    user_type: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    licence_no: Optional[int] = Form(None),
    licence_expiry_date: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    customer_data = customer_schema.CustomerUpdate(
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
    updated = customer_crud.update_customer(db, customer_id, customer_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated

@router.get("/", response_model=List[customer_schema.Customer])
def read_all_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return customer_crud.get_customers(db, skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=customer_schema.Customer)
def read_one_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = customer_crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/{customer_id}")
def delete_customer_api(customer_id: int, db: Session = Depends(get_db)):
    deleted = customer_crud.delete_customer(db, customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

@router.post("/bulk_delete")
def bulk_delete_customer_api(
    customer_ids: List[int] = Form(...),
    db: Session = Depends(get_db),
):
    return customer_crud.bulk_delete_customers(db, customer_ids)
