import os

# Project ka rasta
PROJECT_DIR = os.path.join("projects", "restaurant_delivery_portal_FINAL")

# Files jinme masla hai
FILES_TO_FIX = [
    "app.py",
    "auth_routes.py",
    "menu_routes.py",
    "order_routes.py"
]

def fix_dots():
    print(f"🔧 Starting AUTOMATIC REPAIR on: {PROJECT_DIR}...\n")
    
    if not os.path.exists(PROJECT_DIR):
        print(f"❌ Error: Folder '{PROJECT_DIR}' nahi mila!")
        return

    for filename in FILES_TO_FIX:
        file_path = os.path.join(PROJECT_DIR, filename)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # --- JADOO: Ghalat Imports ko Theek Karna ---
            # "from .config" ko "from config" bana raha hai
            new_content = content.replace("from .config", "from config")
            new_content = new_content.replace("from .extensions", "from extensions")
            new_content = new_content.replace("from .models", "from models")
            
            # Agar koi change hua to save karein
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"✅ FIXED: {filename} (Imports corrected)")
            else:
                print(f"⚡ OK: {filename} (Already correct)")
                
        except Exception as e:
            print(f"⚠️ Could not fix {filename}: {e}")

    print("\n✅ REPAIR COMPLETE! Ab server chalega.")
    print("------------------------------------------------")
    print("Ab ye commands chalayen:")
    print(f"1. cd {PROJECT_DIR}")
    print("2. python app.py")

if __name__ == "__main__":
    fix_dots()