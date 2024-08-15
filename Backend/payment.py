from flask import Flask, request, jsonify
import stripe

app = Flask(__name__)

# Set your secret key. Remember to switch to your live secret key in production!
stripe.api_key = 'sk_test_51Po5tmGagEbazmy87RpCC15fMo1vrSRAKKS44z5bp08i9Wk2SacVGz1OK0rjNt7fprLdoZ6bn76kCqIqqEmI4YAi00P9jKaznC'  # Replace with your actual secret key

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    data = request.json
    amount = data['amount']  # Amount should be in cents

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',  # Change to your desired currency
        )
        return jsonify({'clientSecret': payment_intent['client_secret']})
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
