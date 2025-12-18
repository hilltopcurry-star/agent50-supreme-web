# --- DEBUG ROUTE (ERROR PAKADNE KE LIYE) ---
@routes_bp.route('/create-admin')
def create_admin():
    try:
        # 1. Check agar User table exist karta hai
        try:
            test = User.query.first()
        except Exception as e:
            return f"❌ Database Error: Table shayad nahi bana. Error: {str(e)}"

        # 2. Check agar Admin pehle se hai
        existing_user = User.query.filter_by(username='admin').first()
        if existing_user:
            # Agar password reset karna ho to uncomment karein:
            # existing_user.set_password('pass123')
            # db.session.commit()
            return "⚠️ Admin pehle se mojood hai! Login karein: admin / pass123"

        # 3. Naya User Banayen
        new_user = User(username='admin', email='admin@example.com')
        
        # Password set karne ki koshish
        if hasattr(new_user, 'set_password'):
            new_user.set_password('pass123')
        else:
            return "❌ Error: User model mein 'set_password' function nahi mila!"

        db.session.add(new_user)
        db.session.commit()
        
        return "✅ User Created Successfully! Ab Login karein."

    except Exception as e:
        # Ye asli error screen par dikhayega
        return f"🔥 CRITICAL ERROR: {str(e)}"
