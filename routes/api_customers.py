from flask import Flask, render_template, request, redirect, url_for, send_file
from db import db
from models import Product, Customer
import csv
from pathlib import Path

@app.route("/")
def home():
    return render_template('index.html', name='Ashutosh Dhatwalia') 

@app.route("/customers")    # read customer data from csv and use csv.dictreader to display the data in a table
def customers():
    return render_template('customers.html', customers = Customer.query.all())

@app.route("/products")   # read product data from csv and use csv.dictreader to display the data in a table
def products():
    return render_template('products.html', products = Product.query.all())