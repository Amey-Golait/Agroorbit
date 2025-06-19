from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.models.customer import Customer
from app.utils.security import verify_password
from app.utils.token import create_access_token
from app.database import get_db
from app.dependencies.auth import get_current_customer

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.email == form_data.username).first()

    if not customer or not verify_password(form_data.password, customer.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(customer.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/current")
def get_current_user(current_user: Customer = Depends(get_current_customer)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user