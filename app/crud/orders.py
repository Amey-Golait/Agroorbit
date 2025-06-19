from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from fastapi import HTTPException
from app.models.orders import Order as OrderModel
from app.models.customer import Customer as CustomerModel
from app.models.product import Product as ProductModel
from app.schemas.orders import OrderCreate, OrderUpdate
from typing import List

def generate_order_id() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")

def create_order(db: Session, order_data: OrderCreate, created_by: str):
    if not order_data.product_id or not order_data.quantity:
        raise HTTPException(status_code=400, detail="Product IDs and quantity are required")

    if len(order_data.product_id) != len(order_data.quantity):
        raise HTTPException(status_code=400, detail="product_ids and quantity must be of equal length")

    customer = db.query(CustomerModel).filter_by(id=order_data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=400, detail=f"Customer with ID {order_data.customer_id} not found")

    customer_name = customer.name

    order_items_out = []
    total_quantity = 0
    sub_total = Decimal("0.00")

    for product_id, quantity in zip(order_data.product_id, order_data.quantity):
        product = db.query(ProductModel).filter_by(id=product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail=f"Product with ID {product_id} not found")

        unit_price = Decimal(str(product.unit_price or 0))
        line_total = (unit_price * quantity).quantize(Decimal("0.01"), ROUND_HALF_UP)

        order_items_out.append({
            "product_id": product_id,
            "product_name": product.product_name,
            "quantity": quantity,
            "unit_price": float(unit_price)
        })

        total_quantity += quantity
        sub_total += line_total

    tax_pct = Decimal(str(order_data.tax_percent or 0))
    shipping_charge = Decimal(str(order_data.shipping_charge or 0))
    discount_val = Decimal(str(order_data.discount or 0))
    discount_type = (order_data.discount_type or "flat").lower()

    if discount_type == "percent":
        discount_amount = (sub_total * discount_val / Decimal("100")).quantize(Decimal("0.01"), ROUND_HALF_UP)
    else:
        discount_amount = discount_val.quantize(Decimal("0.01"), ROUND_HALF_UP)

    tax_amount = (sub_total * tax_pct / Decimal("100")).quantize(Decimal("0.01"), ROUND_HALF_UP)
    total_amount = (sub_total + tax_amount + shipping_charge - discount_amount).quantize(Decimal("0.01"), ROUND_HALF_UP)

    delivery_date = order_data.delivery_date or (datetime.now().date() + timedelta(days=7))

    new_order = OrderModel(
        order_id=generate_order_id(),
        customer_id=order_data.customer_id,
        customer_name=customer_name,
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        order_items=order_items_out,
        sub_total=float(sub_total),
        tax_percent=float(tax_pct),
        tax_amount=float(tax_amount),
        shipping_charge=float(shipping_charge),
        discount=float(discount_amount),
        discount_type=discount_type,
        total_amount=float(total_amount),
        payment_status=order_data.payment_status,
        order_status=order_data.order_status,
        payment_mode=order_data.payment_mode,
        order_date=datetime.now(),
        delivery_date=delivery_date,
        created_by=created_by,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def get_order(db: Session, order_id: int):
    order = db.query(OrderModel).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    return order


def get_all_orders(db: Session, skip: int = 0, limit: int = None):
    return db.query(OrderModel).offset(skip).limit(limit).all()


def update_order(db: Session, order_id: int, updates: OrderUpdate):
    order = get_order(db, order_id)
    data = updates.dict(exclude_unset=True)

    for k in list(data):
        v = data[k]
        if v is None or (isinstance(v, str) and not v.strip()):
            data.pop(k)

    for fld in ("payment_status", "order_status", "delivery_date"):
        if fld in data:
            setattr(order, fld, data[fld])

    old_sub_total = Decimal(str(order.sub_total   or 0))
    old_tax_pct   = Decimal(str(order.tax_percent or 0))
    old_ship      = Decimal(str(order.shipping_charge or 0))
    old_disc      = Decimal(str(order.discount       or 0))
    old_disc_type = (order.discount_type or "flat").lower()

    tax_pct = (Decimal(str(data["tax_percent"]))     if "tax_percent"     in data else old_tax_pct)
    ship    = (Decimal(str(data["shipping_charge"])) if "shipping_charge" in data else old_ship)
    disc    = (Decimal(str(data["discount"]))        if "discount"        in data else old_disc)
    disc_type = (data["discount_type"].lower()       if "discount_type"   in data else old_disc_type)

    if disc_type == "percent":
        discount_amount = (old_sub_total * disc / Decimal("100")).quantize(Decimal("0.01"), ROUND_HALF_UP)
    else:
        discount_amount = disc

    tax_amount   = (old_sub_total * tax_pct / Decimal("100")).quantize(Decimal("0.01"), ROUND_HALF_UP)
    total_amount = (old_sub_total + tax_amount + ship - discount_amount).quantize(Decimal("0.01"), ROUND_HALF_UP)

    order.tax_percent     = float(tax_pct)
    order.tax_amount      = float(tax_amount)
    order.shipping_charge = float(ship)
    order.discount        = float(discount_amount)
    order.discount_type   = disc_type
    order.total_amount    = float(total_amount)
    order.updated_at      = datetime.now()

    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    db.delete(order)
    db.commit()
    return order


def bulk_delete_order(db: Session, order_ids: List[int]):
    if not order_ids:
        raise HTTPException(status_code=400, detail="No order IDs provided for deletion")

    db.query(OrderModel).filter(OrderModel.id.in_(order_ids)).delete(synchronize_session=False)
    db.commit()
    return {"deleted_ids": order_ids}
