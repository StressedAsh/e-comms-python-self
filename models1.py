from sqlalchemy import (
    Boolean,
    Float,
    Numeric,
    ForeignKey,
    Integer,
    String,
    Column,
    DECIMAL,
    DateTime,
)
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import functions as func
from db import db
import math


class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    phone = mapped_column(String(10), nullable=False)
    balance = mapped_column(DECIMAL(10, 2), nullable=False, default=0)
    orders = relationship("Order")

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
    price = mapped_column(DECIMAL(10, 2), nullable=False)

    stock = mapped_column(Integer, nullable=False)
    # reference to the relationship between the ProductOrder and Product
    orders = relationship("ProductOrder")


class Order(db.Model):
    id = mapped_column(Integer, primary_key=True)
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False)
    total_value = mapped_column(DECIMAL(10, 3), default=0)
    customer = relationship("Customer", back_populates="orders")
    items = relationship("ProductOrder", cascade="all, delete-orphan")
    created_at = mapped_column(DateTime, default=func.now())
    processed = mapped_column(DateTime, default=None, nullable=True)

    def total(self):
        total = 0
        for item in self.items:
            total += item.product.price * item.quantity
        math.floor(total)
        return total

    # def process(self, method):
    #     if self.processed is not None:
    #         print("order already processed")
    #         return False
    #     if self.customer.balance <= 0:
    #         print("customer balance must be > 0")
    #         return False
    #     for item in self.items:
    #         print(item.product.stock)
    #         if item.quantity > item.product.stock:
    #             if method == "reject":
    #                 return False
    #             elif method == "ignore":
    #                 item.quantity = 0
    #             else:
    #                 item.quantity = item.product.stock
    #         item.product.stock -= item.quantity
    #     db.session.commit()
    #     total = self.total()
    #     print(total)
    #     print(self.customer.balance)
    #     self.customer.balance -= total
    #     self.processed = func.now()
    #     db.session.commit()
    #     print(self.customer.balance)
    #     return True


class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey(Order.id), nullable=False)
    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    quantity = mapped_column(Integer, nullable=False)
    # reference to the relationship between the ProductOrder and product
    product = relationship("Product", back_populates="orders")
    # reference to the relationship between the ProductOrder and order
    order = relationship("Order", back_populates="items")
