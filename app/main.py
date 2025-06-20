import os
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.routers import customer, auth, product, orders, staff
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.models.customer import Customer
from app.models.orders import Order
from app.models.staff import Staff

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Template and static file configuration
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Upload directory configuration
IS_RENDER = os.environ.get("RENDER") == "true"
if IS_RENDER:
    UPLOAD_DIR = "/mnt/data/uploads"
else:
    UPLOAD_DIR = os.path.join("app", "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(product.router)
app.include_router(orders.router)
app.include_router(staff.router)

# Root route with dashboard rendering
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    total_customers = db.query(Customer).count()
    total_orders = db.query(Order).count()
    total_products = db.query(Product).count()
    total_staff = db.query(Staff).count()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "customer_count": total_customers,
        "order_count": total_orders,
        "product_count": total_products,
        "staff_count": total_staff,
    })
