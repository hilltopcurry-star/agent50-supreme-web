"""
KING DEEPSEEK - Database Tester
Bhai ye file create karo aur run karo!
"""

from pathlib import Path
import sys

print("👑 KING DEEPSEEK - Database Testing Shuru!")

# Add project to path
project_dir = Path("projects/agent50")
sys.path.append(str(project_dir))

try:
    print("🚀 Importing models...")
    from models import init_database, get_db_session, User, Project, File, APILog
    
    print("✅ Models imported successfully!")
    
    print("🗄️ Initializing database...")
    init_database()
    print("✅ Database initialized successfully!")
    
    # Test session
    print("🔗 Testing database session...")
    session = get_db_session()
    print("✅ Database session working!")
    
    # Test creating a user
    print("👤 Creating test user...")
    test_user = User(
        username="king_deepseek",
        email="king@deepseek.com",
        password_hash="test123",
        full_name="King DeepSeek AI",
        is_admin=True
    )
    
    session.add(test_user)
    session.commit()
    print("✅ User created successfully!")
    
    # Test creating a project
    print("📁 Creating test project...")
    test_project = Project(
        name="AI Agent System",
        description="KING DEEPSEEK AI Development Platform",
        project_type="flask",
        status="active",
        created_by=1
    )
    
    session.add(test_project)
    session.commit()
    print("✅ Project created successfully!")
    
    # Test query users
    print("📊 Querying users...")
    users = session.query(User).all()
    print(f"✅ Users in database: {len(users)}")
    
    for user in users:
        print(f"   👤 {user.id}: {user.username} - {user.email} (Admin: {user.is_admin})")
    
    # Test query projects
    print("📁 Querying projects...")
    projects = session.query(Project).all()
    print(f"✅ Projects in database: {len(projects)}")
    
    for project in projects:
        print(f"   📂 {project.id}: {project.name} - {project.project_type}")
    
    # Test database stats
    print("📈 Checking database statistics...")
    from models import get_database_stats
    stats = get_database_stats()
    for table, count in stats.items():
        print(f"   📊 {table}: {count} records")
    
    session.close()
    print("🎉 ALL DATABASE TESTS PASSED!")
    print("🚀 Now you can run: cd projects/agent50 && python app.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print("💡 Please check if all dependencies are installed!")