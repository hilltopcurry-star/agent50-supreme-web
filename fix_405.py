import re
from pathlib import Path

# Path to app.py
APP_PATH = Path("projects/Supreme_Food_Delivery/app.py")

if not APP_PATH.exists():
    print("❌ app.py not found")
    exit(1)

with open(APP_PATH, "r", encoding="utf-8") as f:
    content = f.read()

print("🔍 Scanning app.py for Login Route...")

# Regex to find @app.route('/login' ...)
# We want to replace it with @app.route('/login', methods=['GET', 'POST'])
pattern = r"@app\.route\s*\(\s*['\"]/login['\"]\s*(?:,\s*methods=\[.*?\])?\s*\)"
replacement = "@app.route('/login', methods=['GET', 'POST'])"

new_content, count = re.subn(pattern, replacement, content)

if count > 0:
    print("✅ Fixed: Updated /login route to accept POST.")
    with open(APP_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
else:
    print("⚠️ Warning: Could not find /login route to fix. Please check manually.")