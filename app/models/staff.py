from sqlalchemy import Column, Integer, String, Text
from app.database import Base 

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    manager_name = Column(String(100), nullable=True)
    password = Column(Text, nullable=True)
    role = Column(String(50), nullable=True)
