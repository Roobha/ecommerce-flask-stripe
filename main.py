from flask import Flask, render_template, request, redirect, url_for
import stripe
import os
from dotenv import load_dotenv   # ✅ ADD THIS LINE

load_dotenv()                    # ✅ AND THIS LINE

app = Flask(__name__)

# Stripe configuration (test keys)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

# Dummy products data
PRODUCTS = [
    {
        "id": "prod1",
        "name": "Wireless Headphones",
        "description": "Premium wireless headphones with noise cancellation",
        "price": 2499.00,
        "image": "https://plus.unsplash.com/premium_photo-1679513691474-73102089c117?q=80&w=2013&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    },
    {
        "id": "prod2",
        "name": "Smart Watch",
        "description": "Advanced fitness tracking and health monitoring",
        "price": 3499.00,
        "image": "https://images.unsplash.com/photo-1637160151663-a410315e4e75?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    },
    {
        "id": "prod3",
        "name": "Bluetooth Speaker",
        "description": "Portable Bluetooth speaker with HD sound",
        "price": 1599.00,
        "image": "https://images.unsplash.com/photo-1668649175276-fa4f96beb185?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGJsdWV0b290aCUyMHNwZWFrZXJ8ZW58MHx8MHx8fDA%3D"
    },
    {
        "id": "prod4",
        "name": "Laptop Backpack",
        "description": "Stylish and spacious laptop backpack for daily use",
        "price": 999.00,
        "image": "https://images.unsplash.com/photo-1668114844900-537ab91478b9?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fExhcHRvcCUyMEJhY2twYWNrfGVufDB8fDB8fHww"
    },
    {
        "id": "prod5",
        "name": "USB-C Hub",
        "description": "Multiport USB-C hub with HDMI, USB 3.0 and SD card reader",
        "price": 1299.00,
        "image": "https://images.unsplash.com/photo-1616578273577-5d54546f4dec?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8VVNCJTIwQyUyMEh1YnxlbnwwfHwwfHx8MA%3D%3D"
    },
    {
        "id": "prod6",
        "name": "Portable Power Bank",
        "description": "10000mAh fast-charging portable power bank with dual USB output",
        "price": 899.00,
        "image": "https://media.istockphoto.com/id/1220987797/photo/mobile-phone-charging-on-a-portable-power-bank-a-close-up.jpg?s=612x612&w=0&k=20&c=tWFti2o0c3C5KGq_dp9vdplG28cS26SqthPOf2R-X_s="
    }
]

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS, stripe_key=STRIPE_PUBLISHABLE_KEY)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        product_id = request.form['product_id']
        product = next((p for p in PRODUCTS if p['id'] == product_id), None)

        if not product:
            return "Product not found", 404

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': product['name'],
                        'description': product['description'],
                    },
                    'unit_amount': int(product['price'] * 100),  # ₹ to paise
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.host_url + 'success',
            cancel_url=request.host_url + 'cancel',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
