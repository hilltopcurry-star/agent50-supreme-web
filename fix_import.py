from agent_skills import skill_heal_specific_file

# Yeh script Agent ke Healer ko sahi tarah call karega
print("🚑 Starting Healer for Import Error...")

# Hum Agent ko bata rahe hain ke app.py mein 'delivery_bp' ka naam ghalat hai
skill_heal_specific_file(
    'supreme_delivery_app', 
    'app.py', 
    "ImportError: cannot import name 'delivery_bp' from 'routes'. The routes.py likely has a different Blueprint name."
)

print("✅ Fix applied.")