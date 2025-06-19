
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, JSON
from sqlalchemy.sql import func
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(String(20), nullable=True)
    customer_id = Column(Integer, nullable=True)
    customer_name = Column(String(50), nullable=True)
    product_id = Column(JSON, nullable=True)
    quantity = Column(JSON, nullable=True)
    order_items = Column(JSON, nullable=True)
    sub_total = Column(Float, nullable=True)
    tax_percent = Column(Float, nullable=True)
    tax_amount = Column(Float, nullable=True)
    shipping_charge = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)
    discount_type = Column(String(20), nullable=True)
    total_amount = Column(Float, nullable=True)
    payment_status = Column(String(20), nullable=True)
    order_status = Column(String(20), nullable=True)
    payment_mode = Column(String(20), nullable=True)
    order_date = Column(DateTime, nullable=True)
    delivery_date = Column(Date, nullable=True)
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
