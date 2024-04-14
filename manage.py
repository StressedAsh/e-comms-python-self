from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, Column, DECIMAL
from sqlalchemy.orm import relationship, mapped_column
import models
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
                customer = models.Customer(name=i['name'], phone=i['phone'], balance=(1,1000))
                db.session.add(customer)
            db.session.commit()    

def product_table_data():   # this function will be used to populate the product table with data from the csv file 
    with app.app_context():
        with open('./data/products.csv', 'r', newline="") as file:
            reader = csv.DictReader(file)
            for i in reader:
                product = models.Product(name=i['name'], price=i['price'], stock=random.randint(1,100))
                db.session.add(product)
            db.session.commit()

def main(): # this is the main function that will be used to run the above functions, doesnt work if file imported
    drop_tables()
    create_tables()
    customer_table_data()
    product_table_data()

if __name__ == '__main__':
    main()