from fastapi import Form
from pydantic import BaseModel, Field
from typing import Optional, Dict, Union, List
from datetime import date


class ProductBase(BaseModel):
    product_name: Optional[str] = None
    product_code: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    unit: Optional[str] = None
    minimum_purchase_qty: Optional[int] = None
    hsn: Optional[str] = None
    tags: Optional[str] = None
    barcode: Optional[str] = None
    gallery_images: Optional[Union[Dict, str]] = None
    thumbnail_images: Optional[str] = None
    video_provider: Optional[str] = None
    video_link: Optional[str] = None
    colors: Optional[str] = None
    attributes: Optional[str] = None
    unit_price: Optional[float] = None
    box_price: Optional[float] = None
    discount_start_date: Optional[date] = None
    discount_end_date: Optional[date] = None
    discount: Optional[int] = None
    sku: Optional[str] = None
    external_link: Optional[str] = None
    external_link_button_text: Optional[str] = None
    product_description: Optional[str] = None
    pdf_specification: Optional[str] = None
    meta_title: Optional[str] = None
    description: Optional[str] = None
    meta_image: Optional[str] = None
    party_id: Optional[int] = None
    free_shipping: Optional[bool] = None
    flat_rate: Optional[bool] = None
    is_quantity_multiply: Optional[bool] = None
    low_stock_warning: Optional[int] = None
    show_stock_qty: Optional[bool] = None
    show_stock_text_only: Optional[bool] = None
    hide_stock: Optional[bool] = None
    cash_on_delivery: Optional[bool] = None
    is_featured: Optional[bool] = None
    todays_deal: Optional[bool] = None
    flash_deal_title: Optional[str] = None
    flash_discount: Optional[float] = None
    flash_discount_type: Optional[str] = None
    shipping_days: Optional[int] = None
    cgst: Optional[float] = None
    sgst: Optional[float] = None
    tax_type: Optional[str] = Field(None, description="'flat' or 'percentage'")
    published: Optional[bool] = None



class ProductCreate(ProductBase):
    @classmethod
    def as_form(
        cls,
        product_name: Optional[str] = Form(None),
        product_code: Optional[str] = Form(None),
        category: Optional[str] = Form(None),
        brand: Optional[str] = Form(None),
        unit: Optional[str] = Form(None),
        minimum_purchase_qty: Optional[int] = Form(None),
        hsn: Optional[str] = Form(None),
        tags: Optional[str] = Form(None),
        barcode: Optional[str] = Form(None),
        video_provider: Optional[str] = Form(None),
        video_link: Optional[str] = Form(None),
        colors: Optional[str] = Form(None),
        attributes: Optional[str] = Form(None),
        unit_price: Optional[float] = Form(None),
        box_price: Optional[float] = Form(None),
        discount_start_date: Optional[date] = Form(None),
        discount_end_date: Optional[date] = Form(None),
        discount: Optional[int] = Form(None),
        sku: Optional[str] = Form(None),
        external_link: Optional[str] = Form(None),
        external_link_button_text: Optional[str] = Form(None),
        product_description: Optional[str] = Form(None),
        meta_title: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        party_id: Optional[int] = Form(None),
        free_shipping: Optional[bool] = Form(None),
        flat_rate: Optional[bool] = Form(None),
        is_quantity_multiply: Optional[bool] = Form(None),
        low_stock_warning: Optional[int] = Form(None),
        show_stock_qty: Optional[bool] = Form(None),
        show_stock_text_only: Optional[bool] = Form(None),
        hide_stock: Optional[bool] = Form(None),
        cash_on_delivery: Optional[bool] = Form(None),
        is_featured: Optional[bool] = Form(None),
        todays_deal: Optional[bool] = Form(None),
        flash_deal_title: Optional[str] = Form(None),
        flash_discount: Optional[float] = Form(None),
        flash_discount_type: Optional[str] = Form(None),
        shipping_days: Optional[int] = Form(None),
        cgst: Optional[float] = Form(None),
        sgst: Optional[float] = Form(None),
        tax_type: Optional[str] = Form(None),
        published: Optional[bool] = Form(None),
    ):
        return cls(**locals())


class ProductUpdate(ProductCreate):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

def as_form(
    product_id: List[int] = Form(...)
):
    return product_id