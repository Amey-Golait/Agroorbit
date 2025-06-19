from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.staff import StaffCreate, StaffUpdate, StaffOut
from app.crud.staff import (
    create_staff,
    get_staff,
    get_staff_list,
    update_staff,
    delete_staff,
    bulk_delete_staff,
)

router = APIRouter(prefix="/staff", tags=["Staff"])
templates = Jinja2Templates(directory="app/templates")

# === UI Routes ===

@router.get("/ui", response_class=HTMLResponse)
def staff_ui_list(request: Request, db: Session = Depends(get_db)):
    staff = get_staff_list(db)
    return templates.TemplateResponse("staff/staff_table.html", {"request": request, "staff": staff})

# === API Routes ===

@router.post("/", response_model=StaffOut)
def create_staff_api(
    name: str = Form(...),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    manager_name: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    staff_data = StaffCreate(
        name=name,
        email=email,
        phone=phone,
        city=city,
        manager_name=manager_name,
        password=password,
        role=role,
    )
    return create_staff(db, staff_data)


@router.put("/{staff_id}", response_model=StaffOut)
def update_staff_api(
    staff_id: int,
    name: str = Form(...),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    manager_name: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    staff_data = StaffUpdate(
        name=name,
        email=email,
        phone=phone,
        city=city,
        manager_name=manager_name,
        password=password,
        role=role,
    )
    return update_staff(db, staff_id, staff_data)


@router.get("/", response_model=List[StaffOut])
def read_all_staff(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_staff_list(db, skip=skip, limit=limit)


@router.get("/{staff_id}", response_model=StaffOut)
def read_one_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = get_staff(db, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff


@router.delete("/{staff_id}")
def delete_staff_api(staff_id: int, db: Session = Depends(get_db)):
    return delete_staff(db, staff_id)

@router.post("/bulk_delete")
def bulk_delete_staff_api(
    staff_ids: List[int] = Form(...),
    db: Session = Depends(get_db),
):
    return bulk_delete_staff(db, staff_ids)

