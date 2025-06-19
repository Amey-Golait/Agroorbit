from sqlalchemy import Column, Integer, Boolean, Text, Date, Float, JSON
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(Text, nullable=True)
    category = Column(Text, nullable=True)
    brand = Column(Text, nullable=True)
    unit = Column(Text, nullable=True)
    minimum_purchase_qty = Column(Integer, nullable=True)
    hsn = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    barcode = Column(Text, nullable=True)
    gallery_images = Column(JSON, nullable=True)
    thumbnail_images = Column(Text, nullable=True)
    video_provider = Column(Text, nullable=True)
    video_link = Column(Text, nullable=True)
    colors = Column(Text, nullable=True)
    attributes = Column(Text, nullable=True)
    unit_price = Column(Float, nullable=True)
    discount_start_date = Column(Date, nullable=True)
    discount_end_date = Column(Date, nullable=True)
    discount = Column(Integer, nullable=True)
    sku = Column(Text, nullable=True)
    external_link = Column(Text, nullable=True)
    external_link_button_text = Column(Text, nullable=True)
    product_description = Column(Text, nullable=True)
    pdf_specification = Column(Text, nullable=True)
    meta_title = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    meta_image = Column(Text, nullable=True)
    party_id = Column(Integer, nullable=True)

    free_shipping = Column(Boolean, nullable=True)
    flat_rate = Column(Boolean, nullable=True)
    is_quantity_multiply = Column(Boolean, nullable=True)
    low_stock_warning = Column(Integer, nullable=True)

    show_stock_qty = Column(Boolean, nullable=True)
    show_stock_text_only = Column(Boolean, nullable=True)
    hide_stock = Column(Boolean, nullable=True)

    cash_on_delivery = Column(Boolean, nullable=True)
    is_featured = Column(Boolean, nullable=True)
    todays_deal = Column(Boolean, nullable=True)

    flash_deal_title = Column(Text, nullable=True)
    flash_discount = Column(Float, nullable=True)
    flash_discount_type = Column(Text, nullable=True)

    shipping_days = Column(Integer, nullable=True)

    cgst = Column(Float, nullable=True)
    sgst = Column(Float, nullable=True)
    tax_type = Column(Text, nullable=True)
    published = Column(Boolean, nullable=True)
    product_code = Column(Text, nullable=True)
    box_price = Column(Float, nullable=True)
