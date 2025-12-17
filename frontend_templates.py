"""
frontend_templates.py
DEFINES THE SUPREME FRONTEND ARCHITECTURES (V3.0 - FULLY WIRED).
Now includes pre-connected links and working logic. No more manual fixes.
"""

WEB_TEMPLATES = {
    "FOOD_DELIVERY_WEB_SUITE": {
        "description": "Complete Web Suite: Customer Ordering + Restaurant Admin",
        "tech_stack": "HTML5, Bootstrap 5, Chart.js, Socket.IO",
        "files": {
            # --- 1. LOGIN PAGE (PRE-FIXED) ---
            "templates/login.html": { 
                "role": "Universal Login", 
                "instructions": """
Create a Login Page with Tabs (Customer, Restaurant, Driver).
CRITICAL LOGIC:
- JavaScript function login() MUST use fetch('/auth/login', {method:'POST'}).
- MUST include header: 'Content-Type': 'application/json'.
- On success (200), redirect to data.redirect URL immediately.
""" 
            },

            # --- 2. CUSTOMER HOME (PRE-WIRED) ---
            "templates/customer/home.html": { 
                "role": "Landing Page", 
                "instructions": """
Hero Section with Search Bar.
Featured Restaurants Grid.
CRITICAL LOGIC:
- Each Restaurant Card MUST have onclick="window.location.href='/customer/menu'"
- 'Logout' button in Navbar MUST link to href="/".
- 'Profile' button can be href="#".
""" 
            },

            # --- 3. MENU PAGE (PRE-WIRED) ---
            "templates/customer/menu.html": { 
                "role": "Restaurant Menu", 
                "instructions": """
List of Food Items (Burgers, Pizza).
CRITICAL LOGIC:
- 'Add to Cart' button updates a counter variable.
- Bottom Bar shows Total Price.
- Clicking Bottom Bar MUST go to window.location.href='/customer/cart'.
- Back button goes to '/customer/home'.
""" 
            },

            # --- 4. CART PAGE (PRE-WIRED) ---
            "templates/customer/cart.html": { 
                "role": "Checkout", 
                "instructions": """
List selected items.
Address Input field.
CRITICAL LOGIC:
- 'Place Order' button MUST call fetch('/api/orders', {method:'POST'}).
- On success, show alert and redirect to '/customer/home'.
""" 
            },

            # --- 5. RESTAURANT DASHBOARD (PRE-WIRED) ---
            "templates/restaurant/dashboard.html": { 
                "role": "Merchant Dash", 
                "instructions": """
Sidebar with links to Dashboard, Orders, Menu.
Main Content: Live Order Table.
CRITICAL LOGIC:
- JavaScript MUST fetch('/api/restaurant/orders') on load.
- Loop through orders and display in Table.
- Buttons 'Accept'/'Reject' must call API to update status.
""" 
            },

            # --- CSS ---
            "static/css/supreme.css": { 
                "role": "Global Styling", 
                "instructions": ":root { --primary: #00B14F; --dark: #1c1c1c; } body { font-family: 'Segoe UI'; }" 
            }
        }
    }
}

# --- MOBILE TEMPLATES ---
MOBILE_TEMPLATES = {
    "FOOD_DELIVERY_MOBILE_SUITE": {
        "description": "Flutter Apps for Driver and Customer",
        "tech_stack": "Flutter, Google Maps",
        "base_dir": "mobile_apps",
        "files": {
            "pubspec.yaml": { "role": "Deps", "instructions": "http, provider, google_maps_flutter" },
            "lib/main.dart": { "role": "Main", "instructions": "Material App. Home: LoginScreen." },
            "lib/services/api_service.dart": { "role": "API", "instructions": "Base: http://10.0.2.2:5000" }
        }
    }
}