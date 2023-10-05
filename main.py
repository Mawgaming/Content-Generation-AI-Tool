from flask import Flask, request, jsonify
import paypalrestsdk
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import cv2
from transformers import GPT2LMHeadModel, GPT2Tokenizer
mport cv2
import numpy as np
import pyttsx3
mport cv2
import numpy as np
from PIL import Image, ImageFilter
from flask import jsonify

from flask import jsonify




@app.route('/authenticate', methods=['POST'])
def authenticate():
    form_username = request.form.get('username')
    form_password = request.form.get('password')
    user = User.query.filter_by(username=form_username).first()
    if user and bcrypt.check_password_hash(user.password, form_password):
        login_user(user)
        return jsonify({'status': 'Authenticated'})
    return jsonify({'status': 'Authentication failed'})

paypalrestsdk.configure({
  'mode': 'sandbox',
  'client_id': 'YOUR_CLIENT_ID',
  'client_secret': 'YOUR_CLIENT_SECRET'
})

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Add more fields as needed

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    voice_over_time_used = db.Column(db.Integer, default=0)  # Add this line
    # Add more fields as needed


# Initialize the database
db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    form_username = request.form.get('username')
    form_password = request.form.get('password')
    user = User.query.filter_by(username=form_username).first()
    if user and bcrypt.check_password_hash(user.password, form_password):
        login_user(user)
        return jsonify({'status': 'Authenticated'})
    return jsonify({'status': 'Authentication failed'})

@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment = paypalrestsdk.Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'redirect_urls': {
            'return_url': 'http://localhost:5000/payment_success',
            'cancel_url': 'http://localhost:5000/payment_cancel'
        },
        'transactions': [{
            'item_list': {
                'items': [{
                    'name': 'item',
                    'sku': 'item',
                    'price': '5.00',
                    'currency': 'USD',
                    'quantity': 1
                }]
            },
            'amount': {
                'total': '5.00',
                'currency': 'USD'
            },
            'description': 'This is the payment transaction description.'
        }]
    })

    if payment.create():
        print('Payment created successfully')
        for link in payment.links:
            if link.method == 'REDIRECT':
                redirect_url = link.href
                return jsonify({'redirect_url': redirect_url})
    else:
        print(payment.error)
        return jsonify({'status': 'Payment failed'})

# Rest of your original code remains the same

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/generate_text', methods=['POST'])
@login_required
def generate_text():
    # Fetch the current user object from your database
    user = current_user
    
    # Check if the user has remaining voice-over time
    is_allowed, message = check_voice_over_limit(user)
    if not is_allowed:
        return jsonify({'status': 'Limit Reached', 'message': message})

    # Your text and voice-over generation logic here
    # If voice-over is generated, update voice_over_time_used attribute.
    # For instance, if the voice-over took 10 seconds, then:
    user.voice_over_time_used += 10  # or however much time was used
    db.session.commit()

    # Ad placement logic here
    return jsonify({'text': 'Generated Text', 'ad': 'Ad Content'})


@app.route('/generate_voice_over', methods=['POST'])
@login_required  # Assuming the user must be logged in to access this route
def generate_voice_over():
    user = current_user  # Assuming you have a current_user object

    # Logic to check voice-over time limit
    if user.voice_over_time_used >= 300:  # Assuming 300 seconds (or 5 minutes) is the limit
        return jsonify({'status': 'Voice-over time limit reached'})

    # Actual voice-over generation logic here
    # ...

    # Update the voice_over_time_used after successful generation
    user.voice_over_time_used += length_of_voice_over  # Update this variable accordingly
    db.session.commit()  # Don't forget to commit the changes to the database

    return jsonify({'voice_over_url': 'Generated Voice-over URL'})


@app.route('/generate_video', methods=['POST'])
def generate_video():
    # Your video generation logic here
    return jsonify({'video_url': 'Generated Video URL'})

@app.route('/generate_image', methods=['POST'])
def generate_image():
    # Your image generation logic here
    return jsonify({'image_url': 'Generated Image URL'})

@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Your user authentication logic here
    return jsonify({'status': 'Authenticated'})

@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Your payment processing logic here
    return jsonify({'status': 'Payment Processed'})

if __name__ == '__main__':
    app.run(debug=True)
    # Your user authentication logic here
    return jsonify({'status': 'Authenticated'})

@app.route('/paypal_payment', methods=['POST'])
def paypal_payment():
    # Your PayPal payment logic here
    return jsonify({'status': 'Payment Successful'})

@app.route('/google_adsense', methods=['GET'])
def google_adsense():
    # Your Google AdSense logic here
    return jsonify({'ad': 'Ad Content'})

if __name__ == '__main__':
    app.run(debug=True)
