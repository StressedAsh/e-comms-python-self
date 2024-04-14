from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, Column, DECIMAL
from sqlalchemy.orm import relationship, mapped_column

from db import db 

class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    phone = mapped_column(String(10), nullable=False)
    balance  = mapped_column(DECIMAL(10,2), nullable=False, default = 0)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "balance": self.balance,
        }
    
class Product(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    price = mapped_column(DECIMAL(10,2), nullable=False)
    stock = mapped_column(Integer, nullable=False)