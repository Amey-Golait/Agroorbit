from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate
from passlib.context import CryptContext
from app.utils.security import hash_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_staff(db: Session, staff_id: int):
    return db.query(Staff).filter(Staff.id == staff_id).first()


def get_staff_list(db: Session, skip: int = 0, limit: int = None):
    return db.query(Staff).offset(skip).limit(limit).all()


def create_staff(db: Session, staff: StaffCreate):
    password = hash_password(staff.password) if staff.password else None

    db_staff = Staff(
        name=staff.name,
        email=staff.email,
        phone=staff.phone,
        city=staff.city,
        manager_name=staff.manager_name,
        password=password,
        role=staff.role,
    )
    try:
        db.add(db_staff)
        db.commit()
        db.refresh(db_staff)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e.orig)}")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal database error")

    return db_staff


def update_staff(db: Session, staff_id: int, staff: StaffUpdate):
    db_staff = get_staff(db, staff_id)
    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    update_data = staff.dict(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        update_data["password"] = hash_password(update_data.pop("password"))
    elif "password" in update_data:
        update_data.pop("password")

    for key, value in update_data.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            continue
        setattr(db_staff, key, value)

    db.commit()
    db.refresh(db_staff)
    return db_staff


def delete_staff(db: Session, staff_id: int):
    db_staff = get_staff(db, staff_id)
    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    try:
        db.delete(db_staff)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete staff")

    return {"detail": f"Staff with ID {staff_id} deleted successfully"}

def bulk_delete_staff(db: Session, staff_ids: List[int]):
    if not staff_ids:
        raise HTTPException(status_code=400, detail="No staff IDs provided for deletion")

    db.query(Staff).filter(Staff.id.in_(staff_ids)).delete(synchronize_session=False)
    db.commit()
    return {"deleted_ids": staff_ids}
