"""
AGENT 50 - INSTALLATION FIXER
C++ build tools کے بغیر انسٹالیشن فکس کرے گا
"""

import subprocess
import sys
import os
import importlib

def fix_sklearn_installation():
    """scikit-learn انسٹالیشن فکس کریں"""
    print("🔧 FIXING SCIKIT-LEARN INSTALLATION...")
    
    # پہلے ضروری libraries انسٹال کریں
    base_packages = [
        "numpy",
        "scipy",
        "pandas",
        "joblib",
        "threadpoolctl"
    ]
    
    for package in base_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--prefer-binary"])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"⚠️ {package} installation failed, trying without binary...")
            subprocess.call([sys.executable, "-m", "pip", "install", package])
    
    # اب scikit-learn انسٹال کریں
    try:
        print("📦 Installing scikit-learn with pre-compiled wheels...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn", "--prefer-binary", "--no-deps"])
    except subprocess.CalledProcessError:
        print("🔄 Trying alternative method...")
        subprocess.call([sys.executable, "-m", "pip", "install", "scikit-learn", "--no-deps"])
    
    print("🎯 SCIKIT-LEARN INSTALLATION ATTEMPT COMPLETED")

def install_requirements_without_sklearn():
    """scikit-learn کے بغیر requirements انسٹال کریں"""
    print("📥 INSTALLING REQUIREMENTS WITHOUT SCIKIT-LEARN...")
    
    # requirements فائل پڑھیں
    req_path = 'requirements_advanced.txt'
    if not os.path.exists(req_path):
        print(f"❌ {req_path} not found in current folder ({os.getcwd()}). Aborting.")
        return

    with open(req_path, 'r', encoding='utf-8') as f:
        packages = f.readlines()
    
    # scikit-learn کو چھوڑ کر باقی انسٹال کریں
    for package in packages:
        package = package.strip()
        if package and not package.startswith('#') and 'scikit-learn' not in package:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
    
    print("📦 Now installing scikit-learn separately...")
    fix_sklearn_installation()

def check_installation():
    """انسٹالیشن چیک کریں — import اسموں کا درست mapping استعمال کرتا ہے"""
    print("🔍 CHECKING INSTALLATION STATUS...")
    
    # pip package name -> python import name mapping (special cases)
    pkg_import_map = {
        "opencv-python": "cv2",
        "pillow": "PIL",
        "pyjwt": "jwt",       # lowercase key for convenience
        "PyJWT": "jwt",       # keep original name too
        "python-dotenv": "dotenv",
        "flask-socketio": "flask_socketio"
    }
    
    required_packages = [
        "flask", "numpy", "opencv-python", "pillow",
        "sqlalchemy", "requests", "jinja2", "PyJWT"
    ]
    
    missing = []
    results = {}
    for package in required_packages:
        # determine which import name to try
        import_name = pkg_import_map.get(package)
        if not import_name:
            # default: replace hyphens with underscores and try lowercase common name
            import_name = package.replace("-", "_")
        try:
            importlib.import_module(import_name)
            results[package] = True
            print(f"✅ {package} - OK (import as '{import_name}')")
        except Exception:
            # if default failed, try a fallback by trying common variations
            tried = [import_name]
            alt_ok = False
            # try lowercase / upper variations
            alt_candidates = [package.split("-")[-1], package.replace("-", "").lower()]
            for alt in alt_candidates:
                if alt and alt not in tried:
                    try:
                        importlib.import_module(alt)
                        results[package] = True
                        print(f"✅ {package} - OK (import as '{alt}')")
                        alt_ok = True
                        break
                    except Exception:
                        tried.append(alt)
            if not alt_ok:
                missing.append(package)
                results[package] = False
                print(f"❌ {package} - MISSING (tried: {tried})")
    
    if missing:
        print(f"🚨 MISSING PACKAGES: {missing}")
        return False
    else:
        print("🎉 ALL CORE PACKAGES INSTALLED SUCCESSFULLY!")
        return True

if __name__ == "__main__":
    print("👑 AGENT 50 - INSTALLATION FIXER")
    print("=" * 50)
    
    # آپشن منتخب کریں
    print("1. Fix scikit-learn installation")
    print("2. Install all requirements without scikit-learn first")
    print("3. Check installation status")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        fix_sklearn_installation()
    elif choice == "2":
        install_requirements_without_sklearn()
    elif choice == "3":
        check_installation()
    else:
        print("❌ Invalid choice")
    
    # فائنل چیک
    if check_installation():
        print("\n🎯 AGENT 50 READY FOR DEVELOPMENT!")
    else:
        print("\n⚠️ Some packages missing, but core functionality should work")
