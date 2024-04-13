from flask import Flask, render_template, request, redirect, url_for, send_file
import csv

app = Flask(__name__)

@app.route("/")
def home():
    list1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    return render_template('index.html', name='Ashutosh Dhatwalia',passed_value = list1) 

@app.route("/customers")
def customers():
    with open ('data/customers.csv', 'r') as file:
        reader = csv.reader(file) # reader object -> list of lists for all the items in the csv files, puts every line in a list and wraps that in 1 list
        customers = list(reader)
        print(customers)

    return render_template('customers.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)

