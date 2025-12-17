import stripe
from flask import Flask, Blueprint, request, jsonify, current_app
from models import Order
from extensions import db
from config import Config

payment_bp = Blueprint('payment_bp', __name__, url_prefix='/')

class PaymentManager:
    def __init__(self, app):
        self.stripe_secret_key = app.config['STRIPE_SECRET_KEY']
        self.stripe_webhook_secret = app.config['STRIPE_WEBHOOK_SECRET']
        stripe.api_key = self.stripe_secret_key

    def create_checkout_session(self, order_id, user_id):
        try:
            order = Order.query.get(order_id)
            if not order:
                return jsonify({'error': 'Order not found'}), 404

            #  Replace with actual line items from the order
            line_items = [{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Supreme Delivery Order',
                    },
                    'unit_amount': int(order.total_amount * 100),  # Stripe requires amount in cents
                },
                'quantity': 1,
            }]

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.url_root + 'success?session_id={CHECKOUT_SESSION_ID}',  # Replace with your success URL
                cancel_url=request.url_root + 'cancel',  # Replace with your cancel URL
                client_reference_id=order_id,
            )
            return jsonify({'session_id': session.id}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def handle_webhook(self, payload, sig_header):
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.stripe_webhook_secret
            )
        except ValueError as e:
            # Invalid payload
            return jsonify({'error': str(e)}), 400
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return jsonify({'error': str(e)}), 400

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            order_id = session.get('client_reference_id')

            # Fulfill the purchase...
            self.fulfill_order(order_id)

        return jsonify({'status': 'success'}), 200

    def fulfill_order(self, order_id):
        """
        Fulfills the order by updating the order status in the database.
        """
        try:
            order = Order.query.get(order_id)
            if order:
                order.status = 'PAID'  # or 'PROCESSING', etc.
                db.session.commit()
                print(f"Order {order_id} has been successfully paid and updated.")
            else:
                print(f"Order {order_id} not found.")
        except Exception as e:
            print(f"Error fulfilling order {order_id}: {str(e)}")


# Initialize PaymentManager outside the route
payment_manager = None

@payment_bp.record_once
def on_load(state):
    global payment_manager
    payment_manager = PaymentManager(state.app)

@payment_bp.route('/create-checkout/<int:order_id>', methods=['POST'])
def create_checkout(order_id):
    user_id = 1  #  Replace with actual user ID retrieval logic
    return payment_manager.create_checkout_session(order_id, user_id)

@payment_bp.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    return payment_manager.handle_webhook(payload, sig_header)