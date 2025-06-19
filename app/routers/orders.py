from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response, HTMLResponse
from app.schemas.orders import OrderCreate, OrderUpdate, Order
from app.crud.orders import (
    create_order, get_order,
    get_all_orders, update_order, delete_order, bulk_delete_order
)
from app.database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])
templates = Jinja2Templates(directory="app/templates")

# --- UI ROUTES ---

@router.get("/ui", response_class=HTMLResponse)
def order_ui_list(request: Request, db: Session = Depends(get_db)):
    orders = get_all_orders(db)
    return templates.TemplateResponse("order/order_table.html", {"request": request, "orders": orders})

# --- API ROUTES ---
@router.post("/", response_model=Order)
def api_create_order(
    order_data: OrderCreate = Depends(OrderCreate.as_form),
    db: Session = Depends(get_db),
):
    return create_order(db=db, order_data=order_data, created_by="self")

@router.post("/bulk_delete")
def bulk_delete_products(
    order_ids: List[int] = Form(...),
    db: Session = Depends(get_db)
):
    return bulk_delete_order(db, order_ids)

@router.get("/{order_id}", response_model=Order)
def api_get_order(order_id: int, db: Session = Depends(get_db)):
    return get_order(db, order_id)


@router.get("/", response_model=List[Order])
def api_list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_orders(db, skip=skip, limit=limit)


@router.put("/{order_id}", response_model=Order)
def api_update_order(
    order_id: int,
    updates: OrderUpdate = Depends(OrderUpdate.as_form),
    db: Session = Depends(get_db),
):
    return update_order(db, order_id, updates)

@router.delete("/{order_id}", status_code=204)
def api_delete_order(order_id: int, db: Session = Depends(get_db)):
    delete_order(db, order_id)
    return Response(status_code=204)
