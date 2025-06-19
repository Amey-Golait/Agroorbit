from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form, Request
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.crud.product import (
    create_product as crud_create_product,
    get_products as crud_get_products,
    get_product as crud_get_product,
    update_product as crud_update_product,
    delete_product as crud_delete_product,
    bulk_delete_product,
    add_gallery_image,
    update_gallery_image,
    delete_gallery_image,
    bulk_upload_products_logic,
    generate_products_csv
)
from app.database import get_db

router = APIRouter(prefix="/products", tags=["products"])
templates = Jinja2Templates(directory="app/templates")

# === UI Routes ===

@router.get("/ui", response_class=HTMLResponse)
def product_ui_list(request: Request, db: Session = Depends(get_db)):
    products = crud_get_products(db)
    return templates.TemplateResponse("product/product_table.html", {"request": request, "product": products})

# === API Routes ===

@router.post("/", response_model=Product)
async def create_product(
    product_in: ProductCreate = Depends(ProductCreate.as_form),
    gallery_images: Optional[List[UploadFile]] = File(None),
    thumbnail_images: Optional[UploadFile] = File(None),
    meta_image: Optional[UploadFile] = File(None),
    pdf_specification: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    return await crud_create_product(
        db=db,
        product_in=product_in,
        gallery_images=gallery_images,
        thumbnail_images=thumbnail_images,
        meta_image=meta_image,
        pdf_specification=pdf_specification,
    )


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product_in: ProductUpdate = Depends(ProductUpdate.as_form),
    gallery_images: Optional[List[UploadFile]] = File(None),
    thumbnail_images: Optional[UploadFile] = File(None),
    meta_image: Optional[UploadFile] = File(None),
    pdf_specification: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    product = await crud_update_product(
        db=db,
        product_id=product_id,
        product_in=product_in,
        gallery_images=gallery_images,
        thumbnail_images=thumbnail_images,
        meta_image=meta_image,
        pdf_specification=pdf_specification
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=List[Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_get_products(db, skip=skip, limit=limit)

@router.post("/bulk_delete")
def bulk_delete_products(
    product_id: List[int] = Form(...),
    db: Session = Depends(get_db)
):
    return bulk_delete_product(db, product_id)

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud_get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", response_model=Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud_delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/{product_id}/gallery_images", response_model=Product)
async def api_add_gallery_image(product_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    product = await add_gallery_image(db, product_id, file)
    if not product:
        raise HTTPException(404, "Product not found")
    return product

@router.put("/{product_id}/gallery_images/{image_id}", response_model=Product)
async def api_update_gallery_image(
    product_id: int,
    image_id: int,
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    product = await update_gallery_image(db, product_id, image_id, file)
    if not product:
        raise HTTPException(404, "Product or Image ID not found")
    return product

@router.delete("/{product_id}/gallery_images/{image_id}", response_model=Product)
def api_delete_gallery_image(product_id: int, image_id: int, db: Session = Depends(get_db)):
    product = delete_gallery_image(db, product_id, image_id)
    if not product:
        raise HTTPException(404, "Product or Image ID not found")
    return product

@router.post("/bulk_upload")
def bulk_upload_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return bulk_upload_products_logic(file, db)

@router.get("/download/csv", response_class=StreamingResponse)
def download_products_csv(db: Session = Depends(get_db)):
    return generate_products_csv(db)