from flask import Flask, render_template, request, redirect, url_for, send_file
from db import db
from models import Product, Customer
import csv
from pathlib import Path


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"  # this is the path to the database file

app.instance_path = Path("./data").resolve()   # this is the path to the folder where the database file will be stored

db.init_app(app) # this is the database object that will be used to interact with the database

# -------------------------------------------- API --------------------------------------------

@app.route("/")
def home():
    return render_template('index.html', name='Ashutosh Dhatwalia')

# -------------------------------------------- CUSTOMERS --------------------------------------------

@app.route("/customers")    # loads data from db and displays it in a table
def customers(message = ""):
    return render_template('customers.html', customers = Customer.query.all(), message = message)


@app.route("/api/customers/<int:id>", methods = ["GET"])  # this route will return the customer data based on the id
def customer_info(id):
    result = db.get_or_404(Customer, id)
    return render_template("customer.html", customer=result)
    

@app.route("/api/customers", methods = ["GET"])  # this route will return a customer html using button
def customer_info_btn():
    id = request.args.get('id')
    customer_data = db.session.query(Customer).get(id)
    return render_template("customer.html",customer=customer_data)


@app.route("/api/customers", methods = ["POST"])  # this route will add a new customer to the database
def add_customer():
    data = request.get_json()
    customer = Customer(name=data['name'], phone=data['phone'], balance=data['balance'])
    db.session.add(customer)
    db.session.commit()
    return customers("Customer added successfully!")

@app.route("/api/customers/<int:id>", methods = ["DELETE"]) # this route will delete a customer from the database based on the id
def delete_customer(id):
    customer = db.session.query(Customer).get(id)
    db.session.delete(customer)
    db.session.commit()
    return customers("Customer deleted successfully!")

@app.route("/api/customers/<int:id>", methods = ["PUT"])  # this route will update the customer data based on the id
def update_customer(id):
    data = request.get_json()
    customer = db.session.query(Customer).get(id)
    customer.name = data['name']
    customer.phone = data['phone']
    customer.balance = data['balance']
    db.session.commit()
    return customers("Customer updated successfully!")

# -------------------------------------------- PRODUCTS --------------------------------------------

@app.route("/products")   # read product data from csv and use csv.dictreader to display the data in a table
def products(message = ""):
    return render_template('products.html', products = Product.query.all(), message = message)

# -------------------------------------------- END --------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=8080)
