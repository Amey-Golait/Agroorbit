from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.utils.security import hash_password
from typing import List


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = None):
    return db.query(Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: CustomerCreate):
    existing_customer = db.query(Customer).filter(
        or_(
            Customer.email == customer.email,
            Customer.phone == customer.phone
        )
    ).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer with this email or phone already exists")

    hashed_password = hash_password(customer.password)

    customer_data = customer.dict()
    customer_data["password"] = hashed_password
    db_customer = Customer(**customer_data)
    try:
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e.orig)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal database error")
    return db_customer

def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None

    update_data = customer.dict(exclude_unset=True)
   
    if "password" in update_data and update_data["password"]:
        update_data["password"] = hash_password(update_data["password"])
    elif "password" in update_data and not update_data["password"]:
        del update_data["password"]  

    for key, value in update_data.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            continue
        setattr(db_customer, key, value)
            
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    try:
        db.delete(db_customer)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete customer")

    return db_customer

def bulk_delete_customers(db: Session, customer_ids: List[int]):
    if not customer_ids:
        raise HTTPException(status_code=400, detail="No staff IDs provided for deletion")

    db.query(Customer).filter(Customer.id.in_(customer_ids)).delete(synchronize_session=False)
    db.commit()
    return {"deleted_ids": customer_ids}