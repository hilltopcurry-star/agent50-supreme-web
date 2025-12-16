"""
👑 KING DEEPSEEK - Fixed Migration Runner
Bhai ye file create karo aur run karo!
"""

try:
    from migrations.migration_001 import upgrade
    
    print("🚀 Running database migration...")
    if upgrade():
        print("🎉 Migration completed successfully!")
        print("✅ Database is ready!")
        print("🚀 Now run: python app.py")
    else:
        print("💥 Migration failed! Check errors above.")
        
except Exception as e:
    print(f"❌ Migration error: {e}")
    import traceback
    traceback.print_exc()