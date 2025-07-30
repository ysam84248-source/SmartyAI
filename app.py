from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)
ORDERS_FILE = 'orders.json'

def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, 'r') as f:
        return json.load(f)

def save_orders(orders):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/captions', methods=['GET', 'POST'])
def captions():
    caption = None
    if request.method == 'POST':
        product = request.form['product']
        caption = f"🔥 Get your {product} now – Only at Smarty Dropship!"
    return render_template('captions.html', caption=caption)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    orders = load_orders()
    if request.method == 'POST':
        new_order = {
            "name": request.form['name'],
            "product": request.form['product'],
            "address": request.form['address'],
            "payment": request.form['payment'],
            "status": "Pending"
        }
        orders.append(new_order)
        save_orders(orders)
        return redirect('/orders')
    return render_template('orders.html', orders=orders)

if __name__ == '__main__':
    print("👉 Starting SmartyAI Flask Server...")
    app.run(host='0.0.0.0', port=5000)
    