import os

# File Path
file_path = os.path.join("projects", "delivery_production_v2", "payment_handler.py")

# Missing Code to Append
missing_routes = '''

@payment_bp.route('/success', methods=['GET'])
def payment_success():
    return "<h1>Payment Successful! ✅</h1><p>Your order is being processed.</p>"

@payment_bp.route('/cancel', methods=['GET'])
def payment_cancel():
    return "<h1>Payment Cancelled ❌</h1><p>You can try again anytime.</p>"
'''

# Append to file
try:
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(missing_routes)
    print("✅ FIXED: Success and Cancel routes added to payment_handler.py")
except Exception as e:
    print(f"❌ Error: {e}")