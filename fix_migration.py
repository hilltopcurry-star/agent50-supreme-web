"""
KING DEEPSEEK - Migration Fixer
Bhai ye file create karo aur run karo!
"""

from pathlib import Path

print("👑 KING DEEPSEEK - Migration Files Fix Shuru!")

# Project directory
project_dir = Path("projects/agent50")
migrations_dir = project_dir / "migrations"
migrations_dir.mkdir(exist_ok=True)

# Fix 1: Create corrected migration file
migration_file = migrations_dir / "migration_001.py"
migration_code = '''
"""
🤖 AI-Generated Database Migration
KING DEEPSEEK AI Agent - Database Integration
"""

def upgrade():
    """Apply initial migration"""
    print("🚀 Applying initial database migration...")
    try:
        from models import init_database
        init_database()
        print("✅ Database migration completed!")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def downgrade():
    """Rollback migration"""
    print("⚠️ Rolling back migration...")
    import os
    if os.path.exists('app.db'):
        os.remove('app.db')
        print("✅ Database removed!")
    else:
        print("❌ Database file not found!")

if __name__ == "__main__":
    upgrade()
'''

with open(migration_file, 'w', encoding='utf-8') as f:
    f.write(migration_code)
print("✅ migration_001.py file created!")

# Fix 2: Create corrected run_migration.py
runner_file = project_dir / "run_migration.py"
runner_code = '''
from migrations.migration_001 import upgrade

print("🚀 Running database migration...")
if upgrade():
    print("🎉 Migration completed successfully!")
else:
    print("💥 Migration failed!")
'''

with open(runner_file, 'w', encoding='utf-8') as f:
    f.write(runner_code)
print("✅ run_migration.py file updated!")

print("🎯 All migration files fixed successfully!")
print("🚀 Now run: cd projects/agent50 && python run_migration.py")