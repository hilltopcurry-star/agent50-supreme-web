# project_templates.py

PROJECT_SPECS = {
    "food_delivery": {
        "description": "Supreme Delivery App - Phase 2 Production (Week 2)",
        "backend_files": [
            # 1. CORE CONFIGURATION
            {
                "filename": "config.py",
                "role": "Config keys: SECRET_KEY, SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET."
            },
            {
                "filename": "extensions.py",
                "role": "Initialize plugins: db, migrate, jwt, cors, socketio."
            },

            # 2. ADVANCED MODELS (Developer's Module 1.2 & 3.1)
            {
                "filename": "models.py",
                "role": """
                Define Models based on Developer Specs:
                - User: id, username, email, password_hash, role, lat, lng, is_available.
                - Product: id, name, price, stock_quantity, description.
                - Order: id, status, total_amount, delivery_fee, delivery_lat, delivery_lng.
                - Transaction: stripe_payment_intent_id, amount, status.
                - InventoryLog: product_id, quantity_change, reason.
                - OrderStateChange: from_state, to_state, changed_by.
                - Cart & CartItem: Session based shopping cart.
                """
            },

            # 3. PAYMENT MODULE (Developer's Module 1.1)
            {
                "filename": "payment_handler.py",
                "role": """
                Implement Class PaymentManager as per developer specs:
                - create_checkout_session(order_id, user_id)
                - handle_webhook(payload, sig_header)
                - Blueprint: payment_bp (prefix=/payment).
                - Routes: /create-checkout/<order_id>, /webhook.
                NOTE: Use the exact logic provided by the developer for Stripe Sessions.
                """
            },
            {
                "filename": "cart_manager.py",
                "role": """
                Implement Class CartManager:
                - get_or_create_cart()
                - add_to_cart()
                - convert_cart_to_order()
                """
            },

            # 4. REAL-TIME MODULE (Developer's Module 2.1)
            {
                "filename": "socketio_handler.py",
                "role": """
                Implement Real-Time Logic:
                - init_socketio(app)
                - @socketio.on('connect'): Auth check.
                - @socketio.on('driver_location_update'): Update DB & Emit.
                - emit_order_status_change()
                """
            },

            # 5. BUSINESS LOGIC MODULES (Developer's Module 3 & 4)
            {
                "filename": "state_machine.py",
                "role": """
                Implement Class OrderStateMachine:
                - TRANSITIONS dictionary.
                - transition(order, new_state).
                - Logic for inventory hold/release.
                """
            },
            {
                "filename": "geolocation.py",
                "role": """
                Implement Class GeoLocationService:
                - haversine_distance()
                - calculate_delivery_fee()
                - find_nearby_drivers()
                """
            },

            # 6. APP FACTORY & ROUTES
            {
                "filename": "routes.py",
                "role": "Main Web Routes using StateMachine and CartManager."
            },
            {
                "filename": "api_routes.py",
                "role": "Mobile API Routes (Login, Order History)."
            },
            {
                "filename": "app.py",
                "role": """
                Main Entry Point:
                - Init socketio via socketio_handler.init_socketio(app).
                - Register all Blueprints.
                - Import 'socketio_handler' and 'payment_handler'.
                - CRITICAL: Run using socketio.run(app) instead of app.run().
                """
            }
        ],
        "web_template": {
            "files": {
                "templates/base.html": {"instructions": "Base layout."},
                "templates/checkout.html": {"instructions": "Stripe payment page."},
                "templates/tracking.html": {"instructions": "Real-time map tracking page."},
                "templates/dashboard_admin.html": {"instructions": "Admin view for Analytics."}
            }
        },
        "required_packages": [
            "Flask", "Flask-SQLAlchemy", "Flask-Migrate", "Flask-Cors", 
            "Flask-JWT-Extended", "Flask-SocketIO", "stripe", "geopy", "eventlet"
        ]
    }
}