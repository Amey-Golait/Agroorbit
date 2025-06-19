from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    firm_name = Column(String(255), nullable=True)
    phone = Column(String(50), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    pan_no = Column(String(50), nullable=True)
    user_type = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)
    licence_no = Column(Integer, nullable=True)
    licence_expiry_date = Column(Date, nullable=True)
    password = Column(String(255), nullable=True)
