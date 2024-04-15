from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, Column, DECIMAL, func
from sqlalchemy.orm import relationship, mapped_column
from models import Customer, Product, Order, ProductOrder
from db import db
from app import app
import csv
import random

def create_tables(): # this function will be used to create all the tables in the database
    with app.app_context():
        db.create_all()

def drop_tables():  # this function will be used to drop all the tables in the database
    with app.app_context():
        db.drop_all()

def customer_table_data():  # this function will be used to populate the customer table with data from the csv file
    with app.app_context():
        with open('./data/customers.csv', 'r', newline="") as file:
            reader = csv.DictReader(file)
            for i in reader:
                customer = Customer(name=i['name'], phone=i['phone'], balance=(random.randint(1,999))) # balance is a random number between 200 and 10000
                db.session.add(customer)
            db.session.commit()    

def product_table_data():   # this function will be used to populate the product table with data from the csv file 
    with app.app_context():
        with open('./data/products.csv', 'r', newline="") as file:
            reader = csv.DictReader(file)
            for i in reader:
                product = Product(name=i['name'], price=i['price'], stock=random.randint(1,100))
                db.session.add(product)
            db.session.commit()

def order_table_data():  # this function will be used to populate the order table with data randomly generated
    with app.app_context():
        for i in range(10):
            customer_statement = db.select(Customer).order_by(func.random()).limit(1)
            customer_data = db.session.execute(customer_statement).scalar()
            order = Order(customer = customer_data)
            db.session.add(order)
            product_statement = db.select(Product).order_by(func.random()).limit(1)
            product_data = db.session.execute(product_statement).scalar()
            random_quantity = random.randint(1, 10)
            product_order_data = ProductOrder(order = order, product = product_data, quantity = random_quantity)
            db.session.add(product_order_data)
            product_statement = db.select(Product).order_by(func.random()).limit(1)
            product_data = db.session.execute(product_statement).scalar()
            random_quantity = random.randint(1, 10)
            product_order_data = ProductOrder(order = order, product = product_data, quantity = random_quantity)
            db.session.add(product_order_data)
            order.order_total = order.total()
        db.session.commit()

def main(): # this is the main function that will be used to run the above functions, doesnt work if file imported
    drop_tables()
    create_tables()
    customer_table_data()
    product_table_data()
    order_table_data()
    print("Tables created and data inserted successfully")

if __name__ == '__main__':
    main()
