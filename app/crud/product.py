import os
import re
import math
from fastapi.responses import StreamingResponse
import csv  
import pandas as pd
from io import BytesIO, StringIO
import json
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

UPLOAD_BASE = "uploads"
FOLDERS = {
    "gallery_images": "gallery_images",
    "thumbnail_images": "thumbnail_images",
    "meta_image": "meta_image",
    "pdf_specification": "pdf_specification"
}

# --------------------
# HELPER FUNCTIONS
# --------------------

# Sanitize filename to ensure it is safe for storage
def sanitize_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', name)
    return f"{safe_name}{ext}"

# Save file to the specified folder and return the URL
async def save_file(upload_file: UploadFile, folder_name: str) -> str:
    folder_path = os.path.join(UPLOAD_BASE, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    safe_filename = sanitize_filename(upload_file.filename)
    file_path = os.path.join(folder_path, safe_filename)

    with open(file_path, "wb") as f:
        content = await upload_file.read()
        f.write(content)

    relative_path = os.path.join(folder_name, safe_filename).replace("\\", "/")
    return f"http://127.0.0.1:8000/uploads/{relative_path}"

# Save gallery images and return a list of image details
async def save_gallery_images(files: Optional[List[UploadFile]]) -> dict:
    if not files:
        return {"images": []}

    images_list = []
    for idx, file in enumerate(files, start=1):
        saved_path = await save_file(file, FOLDERS["gallery_images"])
        filename = os.path.basename(saved_path)
        images_list.append({
            "image_id": idx,
            "File-name": filename,
            "url": saved_path  
        })
    
    return {"images": images_list}

# Delete file from the server based on its URL
def delete_file_from_url(url: str):
    if not url:
        return
    try:
        rel_path = url.replace("http://127.0.0.1:8000/uploads/", "")
        abs_path = os.path.join(UPLOAD_BASE, rel_path)
        if os.path.exists(abs_path):
            os.remove(abs_path)
    except Exception:
        pass


# --------------------
# CRUD OPERATIONS
# --------------------

# Create product
async def create_product(
    db: Session,
    product_in: ProductCreate,
    gallery_images: Optional[List[UploadFile]] = None,
    thumbnail_images: Optional[UploadFile] = None,
    meta_image: Optional[UploadFile] = None,
    pdf_specification: Optional[UploadFile] = None
):
    product_data = product_in.dict()

    # Save gallery images
    product_data["gallery_images"] = await save_gallery_images(gallery_images)

    # Save other media files
    if thumbnail_images:
        product_data["thumbnail_images"] = await save_file(thumbnail_images, FOLDERS["thumbnail_images"])
    if meta_image:
        product_data["meta_image"] = await save_file(meta_image, FOLDERS["meta_image"])
    if pdf_specification:
        product_data["pdf_specification"] = await save_file(pdf_specification, FOLDERS["pdf_specification"])

    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# Get single product
def get_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product and product.gallery_images:
        if isinstance(product.gallery_images, str):
            try:
                product.gallery_images = json.loads(product.gallery_images)
            except json.JSONDecodeError:
                product.gallery_images = {"images": []}
    return product


# Get multiple products
def get_products(db: Session, skip: int = 0, limit: int = None):
    products = db.query(Product).offset(skip).limit(limit).all()
    for p in products:
        if p.gallery_images:
            if isinstance(p.gallery_images, str):
                try:
                    p.gallery_images = json.loads(p.gallery_images)
                except json.JSONDecodeError:
                    p.gallery_images = {"images": []}
            elif not isinstance(p.gallery_images, dict):
                p.gallery_images = {"images": []}
    return products

# Update product
async def update_product(
    db: Session,
    product_id: int,
    product_in: ProductUpdate,
    gallery_images: Optional[List[UploadFile]] = None,
    thumbnail_images: Optional[UploadFile] = None,
    meta_image: Optional[UploadFile] = None,
    pdf_specification: Optional[UploadFile] = None,
):
    product = get_product(db, product_id)
    if not product:
        return None

    data = {k: v for k, v in product_in.dict(exclude_unset=True).items() if v is not None}

    if gallery_images:
    
        if isinstance(product.gallery_images, str):
            old_gallery = json.loads(product.gallery_images)
        else:
            old_gallery = product.gallery_images or {"images": []}

        for img in old_gallery.get("images", []):
            delete_file_from_url(img.get("url"))
        
        data["gallery_images"] = await save_gallery_images(gallery_images)

    if thumbnail_images:
        delete_file_from_url(product.thumbnail_images)
        data["thumbnail_images"] = await save_file(thumbnail_images, FOLDERS["thumbnail_images"])
    if meta_image:
        delete_file_from_url(product.meta_image)
        data["meta_image"] = await save_file(meta_image, FOLDERS["meta_image"])
    if pdf_specification:
        delete_file_from_url(product.pdf_specification)
        data["pdf_specification"] = await save_file(pdf_specification, FOLDERS["pdf_specification"])

    for field, value in data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

# Delete product
def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if not product:
        return None

    try:
        gallery = product.gallery_images

        if isinstance(gallery, str):
            gallery = json.loads(gallery)

        for img in gallery.get("images", []):
            if isinstance(img, dict):
                delete_file_from_url(img.get("url"))

        delete_file_from_url(product.thumbnail_images)
        delete_file_from_url(product.meta_image)
        delete_file_from_url(product.pdf_specification)

    except Exception as e:
        print("Error deleting associated media:", e)

    db.delete(product)
    db.commit()
    return product

def bulk_delete_product(db: Session, product_id: List[int]):
    if not product_id:
        raise HTTPException(status_code=400, detail="No staff IDs provided for deletion")

    db.query(Product).filter(Product.id.in_(product_id)).delete(synchronize_session=False)
    db.commit()
    return {"deleted_ids": product_id}

# Add gallery image
async def add_gallery_image(db: Session, product_id: int, file: UploadFile):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    gallery = product.gallery_images or '{"images": []}'
    if isinstance(gallery, str):
        try:
            gallery = json.loads(gallery)
        except json.JSONDecodeError:
            gallery = {"images": []}

    images = gallery.get("images", [])
    max_id = max([img["image_id"] for img in images], default=0)

    url = await save_file(file, FOLDERS["gallery_images"])
    filename = os.path.basename(url)

    new_image = {
        "image_id": max_id + 1,
        "File-name": filename,
        "url": url,
    }
    images.append(new_image)

    product.gallery_images = json.dumps({"images": images})
    db.commit()
    db.refresh(product)
    return product

# Update gallery image
async def update_gallery_image(db: Session, product_id: int, image_id: int, file: UploadFile = None):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    gallery = product.gallery_images or '{"images": []}'
    if isinstance(gallery, str):
        try:
            gallery = json.loads(gallery)
        except json.JSONDecodeError:
            gallery = {"images": []}

    images = gallery.get("images", [])
    updated = False

    for img in images:
        if img["image_id"] == image_id:
            if file:
                delete_file_from_url(img.get("url"))
                saved_url = await save_file(file, FOLDERS["gallery_images"])
                filename = os.path.basename(saved_url)
                img["File-name"] = filename
                img["url"] = saved_url
            updated = True
            break

    if not updated:
        return None

    product.gallery_images = json.dumps({"images": images})
    db.commit()
    db.refresh(product)
    return product

# Delete gallery image
def delete_gallery_image(db: Session, product_id: int, image_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    gallery = product.gallery_images or '{"images": []}'
    if isinstance(gallery, str):
        try:
            gallery = json.loads(gallery)
        except json.JSONDecodeError:
            gallery = {"images": []}

    images = gallery.get("images", [])
    new_images = []
    deleted = False

    for img in images:
        if img["image_id"] == image_id:
            delete_file_from_url(img.get("url"))
            deleted = True
        else:
            new_images.append(img)

    if not deleted:
        return None

    product.gallery_images = json.dumps({"images": new_images})
    db.commit()
    db.refresh(product)
    return product

def _to_python_value(val):
    """Convert pandas NaN (or other non‑scalars) to Python types."""
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    return val

def bulk_upload_products_logic(file: UploadFile, db: Session):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Only .csv or .xlsx files are supported.")

    try:
        content = file.file.read()
        df = pd.read_csv(BytesIO(content)) if file.filename.endswith('.csv') else pd.read_excel(BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    # Mapping from file to model fields
    column_map = {
        'product_name': 'product_name',
        'variant': 'sku',
        'product_code': 'product_code',
        'Quantity In Box': 'minimum_purchase_qty',
        'HSN Code': 'hsn',
        'BOX PRICE': 'box_price',
        'SINGLE PRICE': 'unit_price',
        'Box Unit': 'unit'
    }

    missing_cols = [col for col in column_map if col not in df.columns]
    if missing_cols:
        raise HTTPException(status_code=422, detail=f"Missing columns: {', '.join(missing_cols)}")

    df = df[list(column_map.keys())].rename(columns=column_map)
    df = df.dropna(subset=['product_name', 'sku', 'unit_price'])

    inserted, skipped = 0, 0
    for _, row in df.iterrows():
        sku = _to_python_value(row['sku'])
        if db.query(Product).filter(Product.sku == sku).first():
            skipped += 1
            continue

        product = Product(
            product_name=_to_python_value(row['product_name']),
            sku=sku,
            product_code=_to_python_value(row.get('product_code')),
            minimum_purchase_qty=_to_python_value(row.get('minimum_purchase_qty')),
            hsn=_to_python_value(row.get('hsn')),
            box_price=_to_python_value(row.get('box_price')),
            unit_price=_to_python_value(row.get('unit_price')),
            unit=_to_python_value(row.get('unit'))
        )
        db.add(product)
        inserted += 1

    db.commit()
    return {"success": True, "inserted": inserted, "skipped": skipped}

def generate_products_csv(db: Session):
    products = db.query(Product).all()

    output = StringIO()
    writer = csv.writer(output)

    headers = [
        "id", "product_name", "product_code", "category", "brand", "unit", "minimum_purchase_qty",
        "hsn", "tags", "barcode", "thumbnail_images", "video_provider", "video_link",
        "colors", "attributes", "unit_price", "box_price", "discount_start_date", "discount_end_date",
        "discount", "sku", "external_link", "external_link_button_text", "product_description",
        "pdf_specification", "meta_title", "description", "meta_image", "party_id", "free_shipping",
        "flat_rate", "is_quantity_multiply", "low_stock_warning", "show_stock_qty",
        "show_stock_text_only", "hide_stock", "cash_on_delivery", "is_featured", "todays_deal",
        "flash_deal_title", "flash_discount", "flash_discount_type", "shipping_days",
        "cgst", "sgst", "tax_type", "published", "gallery_images"
    ]
    writer.writerow(headers)

    for p in products:
        gallery_images_serialized = json.dumps(p.gallery_images) if p.gallery_images else ""

        row = [
            p.id, p.product_name, p.product_code, p.category, p.brand, p.unit, p.minimum_purchase_qty,
            p.hsn, p.tags, p.barcode, p.thumbnail_images, p.video_provider, p.video_link,
            p.colors, p.attributes, p.unit_price, p.box_price, p.discount_start_date,
            p.discount_end_date, p.discount, p.sku, p.external_link, p.external_link_button_text,
            p.product_description, p.pdf_specification, p.meta_title, p.description,
            p.meta_image, p.party_id, p.free_shipping, p.flat_rate, p.is_quantity_multiply,
            p.low_stock_warning, p.show_stock_qty, p.show_stock_text_only, p.hide_stock,
            p.cash_on_delivery, p.is_featured, p.todays_deal, p.flash_deal_title,
            p.flash_discount, p.flash_discount_type, p.shipping_days, p.cgst, p.sgst,
            p.tax_type, p.published, gallery_images_serialized
        ]
        writer.writerow(row)

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products.csv"}
    )