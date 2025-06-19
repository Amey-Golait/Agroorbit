from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.database import get_db
from app.utils.token import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Customer:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        customer_id: str = payload.get("sub")
        if customer_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    customer = db.query(Customer).filter(Customer.id == int(customer_id)).first()
    if not customer:
        raise HTTPException(status_code=401, detail="User not found")
    return customer
