# project_templates.py - UPDATED WITH GUARANTEED WORKING LOGIN

PROJECT_SPECS = {
    "food_delivery": {
        "backend_files": [
            {
                "filename": "config.py",
                "role": "Configuration settings. MUST set SECRET_KEY and SQLALCHEMY_DATABASE_URI."
            },
            {
                "filename": "extensions.py",
                "role": "Initialize Flask extensions. MUST use: from flask_bootstrap import Bootstrap (NOT Bootstrap5)."
            },
            {
                "filename": "models.py", 
                "role": "Database models: User(id, username, email), Order(user_id, menu_item_id, quantity)."
            },
            {
                "filename": "routes.py",
                "role": "CRITICAL: Login at /login (NOT /auth/login). MUST return HTML form for GET, handle JSON for POST. Homepage at / MUST return simple HTML (NO render_template)."
            },
            {
                "filename": "app.py",
                "role": "Application Factory. MUST import main_bp (NOT bp). Register blueprint WITHOUT url_prefix. Include error handlers."
            }
        ],
        "web_template": {
            "files": {
                "templates/index.html": {
                    "instructions": "SIMPLE homepage with working login link. MUST contain: <a href='/login'>Login</a> that actually works."
                },
                "templates/login.html": {
                    "instructions": "GUARANTEED WORKING login form. MUST have: 1. POST action='/login', 2. username field, 3. email field, 4. Working submit button. Include JavaScript for AJAX login."
                }
            }
        }
    }
}