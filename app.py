from flask import Flask, render_template, request, redirect, url_for, send_file
from db import db
import requests
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
    customer_data = db.get_or_404(Customer,id)
    return render_template("customer.html",customer=customer_data)


@app.route("/api/customers", methods = ["POST"])  # this route will add a new customer to the database
def add_customer():
    data = request.get_json()
    if data == None:   
        return customers("You must provide data to add a customer! Adding customer was unsuccessful!"), 400
    
    if 'name' not in data or 'phone' not in data:
        return customers("All fields are required! Adding customer was unsuccessful!"), 400
    
    elif type(data["name"]) == str or type(data["phone"]) == str:
        return customers("Name and phone must be string! Adding customer was unsuccessful!"), 400

    if "balance" not in data:
        data['balance'] = 0
    
    elif type(data["balance"]) == int or type(data["balance"]) == str:
        return customers("Balance must be float! Adding customer was unsuccessful!"), 400

    elif data["balance"] < 0:
        return customers("Balance must be positive! Adding customer was unsuccessful!"), 400

    elif len(data['phone']) != 10:
        return customers("Phone number must be 10 digits long! Adding customer was unsuccessful!"), 400
    
    customer = Customer(name=data['name'], phone=data['phone'], balance=data['balance'])
    db.session.add(customer)
    db.session.commit()
    return customers("Customer added successfully!"), 201

@app.route("/api/customers/<int:id>", methods = ["DELETE"]) # this route will delete a customer from the database based on the id
def delete_customer(id):
    if id == None:
        return customers("All fields are required! Delete was unsuccessful!"), 404
    customer = db.get_or_404(Customer, id)
    db.session.delete(customer)
    db.session.commit()
    return customers("Customer deleted successfully!"), 204


@app.route("/api/customers/<int:id>", methods = ["PUT"])  # this route will update the customer data based on the id
def update_customer_balance(id):
    data = request.get_json()
    if data == None:
        return customers("Some data is required for updating the customer. Update was unsuccessful!"), 400
    customer = db.get_or_404(id)
    if len(data) != 1:
        return customers("Only balance can be updated! Update was unsuccessful"), 400
    elif 'balance' not in data:
        return customers("Only balance can be updated! Update was unsuccessful!"), 400
    elif type(data['balance']) != float:
        return customers("Balance must be float! Update was unsuccessful!"), 400
    elif data['balance'] < 0:
        return customers("Balance must be positive! Update was unsuccessful!"), 400
    else:
        customer.balance = data['balance']
    db.session.commit()
    return customers('Customer updated successfully!'), 204


# -------------------------------------------- PRODUCTS --------------------------------------------

@app.route("/products")   # read product data from csv and use csv.dictreader to display the data in a table
def products(message = ""):
    return render_template('products.html', products = Product.query.all(), message = message)


@app.route("/api/products", methods = ["POST"])  # this route will add a new product to the database
def add_product():
    data = request.get_json()
    if data == None:
        return products("You must provide data to add a product! Adding product was unsuccessful!"), 400
    
    elif "name" not in data or "price" not in data:
        return products("All fields are required! Adding product was unsuccessful!"), 400
    
    elif not isinstance(data["name"], str) or not isinstance(data["price"], float):
        return products("Name must be string and price must be float! Adding product was unsuccessful!"), 400
    
    elif "stock" not in data:
        data['stock'] = 0

    elif type(data["stock"]) != int:
        return products("Stock must be integer! Adding product was unsuccessful!"), 400
    
    elif data["stock"] < 0:
        return products("Stock must be positive! Adding product was unsuccessful!"), 400

    product = Product(name=data['name'], price=data['price'], stock=data['stock'])
    db.session.add(product)
    db.session.commit()
    return products("Product added successfully!"), 201


@app.route("/api/products/<int:id>", methods = ["DELETE"])  # this route will delete a product from the database based on the id
def delete_product(id):
    product = db.get_or_404(Product,id)
    db.session.delete(product)
    db.session.commit()
    return products("Product deleted successfully!"), 204


@app.route("/api/products/<int:id>", methods = ["PUT"])  # this route will update the product data based on the id
def update_product(id):
    if id == None:
        return products("All fields are required! Update was unsuccessful!"), 400
    data = request.get_json()
    product = db.get_or_404(Product, id)
    if "name" not in data and "price" not in data and "stock" not in data:
        return products("All fields are required! Update was unsuccessful!"), 400
    
    elif "name" in data and not isinstance(data["name"], str):
        return products("Name must be string! Update was unsuccessful!"), 400
    
    elif "price" in data and not isinstance(data["price"], float):
        return products("Price must be float! Update was unsuccessful!"), 400
    
    elif "stock" in data and not isinstance(data["stock"], int):
        return products("Stock must be integer! Update was unsuccessful!"), 400

    if "name" in data:
        product.name = data['name']
    if "price" in data:
        product.price = data['price']
    if "stock" in data:
        product.stock = data['stock']

    db.session.commit()
    print(product.name)
    return products("Product updated successfully!"), 204


# -------------------------------------------- END --------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=8080)
