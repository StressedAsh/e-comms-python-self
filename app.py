from flask import Flask, render_template, request, redirect, url_for, send_file
from db import db

import csv
from pathlib import Path


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"  # this is the path to the database file

app.instance_path = Path("./data").resolve()   # this is the path to the folder where the database file will be stored

db.init_app(app) # this is the database object that will be used to interact with the database

# all of this bs will be moved to another file and directory in the blueprint section sooner or later

@app.route("/")
def home():
    return render_template('index.html', name='Ashutosh Dhatwalia') 

@app.route("/customers")    # read customer data from csv and use csv.dictreader to display the data in a table
def customers():
    customers_info = []
    with open('./data/customers.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            customers_info.append(row)

    return render_template('customers.html', customers = customers_info)

@app.route("/products")   # read product data from csv and use csv.dictreader to display the data in a table
def products():
    products_info = []
    with open('./data/products.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products_info.append(row)

    return render_template('products.html', products = products_info)


# this the limit, remove everything above this to put this to another file.

if __name__ == '__main__':
    app.run(debug=True, port=8080)

