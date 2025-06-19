from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from fastapi import Form
import json

# Enums
class PaymentStatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"


class OrderStatusEnum(str, Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class PaymentModeEnum(str, Enum):
    cash = "cash"
    card = "card"
    upi = "upi"
    net_banking = "net_banking"

class OrderItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float

# Shared base
class OrderBase(BaseModel):
    order_id: Optional[str] = None
    customer_id: Optional[int] = None
    order_items: List[OrderItem]
    sub_total: Optional[float] = None
    tax_percent: Optional[float] = None
    tax_amount: Optional[float] = None
    shipping_charge: Optional[float] = None
    discount: Optional[float] = None
    discount_type: Optional[str] = None
    total_amount: Optional[float] = None
    payment_status: Optional[PaymentStatusEnum] = PaymentStatusEnum.pending
    order_status: Optional[OrderStatusEnum] = OrderStatusEnum.pending
    payment_mode: Optional[PaymentModeEnum] = PaymentModeEnum.cash
    order_date: Optional[datetime] = None
    delivery_date: Optional[date] = None
    created_by: Optional[str] = None


# Create input
class OrderCreate(BaseModel):
    customer_id: int
    product_id: List[int]
    quantity: List[int]
    payment_status: PaymentStatusEnum = PaymentStatusEnum.pending
    order_status: OrderStatusEnum = OrderStatusEnum.pending
    payment_mode: PaymentModeEnum = PaymentModeEnum.cash
    delivery_date: Optional[date] = None
    tax_percent: Optional[float] = None
    discount: Optional[float] = None
    discount_type: Optional[str] = None
    shipping_charge: Optional[float] = None

    @classmethod
    def as_form(
        cls,
        customer_id: int = Form(...),
        product_id: str = Form(...),
        quantity: str = Form(...),
        payment_status: PaymentStatusEnum = Form(PaymentStatusEnum.pending),
        order_status: OrderStatusEnum = Form(OrderStatusEnum.pending),
        payment_mode: PaymentModeEnum = Form(PaymentModeEnum.cash),
        delivery_date: Optional[date] = Form(None),
        tax_percent: Optional[float] = Form(None),
        shipping_charge: Optional[float] = Form(None),
        discount: Optional[float] = Form(None),
        discount_type: Optional[str] = Form(None),
    ):
        def parse_array(data: str) -> List[int]:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return [int(i.strip()) for i in data.split(",") if i.strip()]

        try:
            product_id_list = parse_array(product_id)
            quantity_list = parse_array(quantity)
        except Exception as e:
            raise ValueError(f"Invalid product_id or quantity: {e}")

        if len(product_id_list) != len(quantity_list):
            raise ValueError("product_id and quantity count mismatch")

        return cls(
            customer_id=customer_id,
            product_id=product_id_list,
            quantity=quantity_list,
            payment_status=payment_status,
            order_status=order_status,
            payment_mode=payment_mode,
            delivery_date=delivery_date,
            tax_percent=tax_percent,
            discount=discount,
            discount_type=discount_type,
            shipping_charge=shipping_charge,
        )


# Update input
class OrderUpdate(BaseModel):
    payment_status: Optional[PaymentStatusEnum] = None
    order_status: Optional[OrderStatusEnum] = None
    delivery_date: Optional[date] = None
    tax_percent: Optional[float] = None
    discount: Optional[float] = None
    discount_type: Optional[str] = None
    shipping_charge: Optional[float] = None

    @classmethod
    def as_form(
        cls,
        payment_status: Optional[PaymentStatusEnum] = Form(None),
        order_status: Optional[OrderStatusEnum] = Form(None),
        delivery_date: Optional[date] = Form(None),
        tax_percent: Optional[float] = Form(None),
        discount: Optional[float] = Form(None),
        discount_type: Optional[str] = Form(None),
        shipping_charge: Optional[float] = Form(None),
    ):
        return cls(
            payment_status=payment_status,
            order_status=order_status,
            delivery_date=delivery_date,
            tax_percent=tax_percent,
            discount=discount,
            discount_type=discount_type,
            shipping_charge=shipping_charge,
        )

# Output schema
class Order(OrderBase):
    id: int
    product_id : List[int]
    quantity : List[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

def as_form(
    order_id: List[int] = Form(...),
):
    return order_id