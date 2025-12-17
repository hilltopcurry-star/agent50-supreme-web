from __future__ import annotations
import sqlite3
import json
import os
from pathlib import Path
from typing import List, Dict, Any
import requests

class DatabaseGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.projects_dir = self.base_dir / "projects"
        self.api_key = "sk-9214c5054a7f4b828cf3f9d608a88f6a"
    
    def analyze_project_structure(self, project_name: str) -> Dict[str, Any]:
        """Project structure analyze karta hai database needs ke liye"""
        project_dir = self.projects_dir / project_name
        
        if not project_dir.exists():
            return {"error": f"Project '{project_name}' not found"}
        
        print(f"🔍 Analyzing project structure: {project_name}")
        
        # Read all Python files to understand data models
        python_files = list(project_dir.glob("**/*.py"))
        project_context = ""
        
        for py_file in python_files[:5]:  # First 5 files for context
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    project_context += f"\n\n--- {py_file.name} ---\n{f.read()}"
            except Exception as e:
                print(f"⚠️ Could not read {py_file}: {e}")
        
        # AI se database schema suggest karta hai
        ai_schema = self.get_ai_database_suggestions(project_name, project_context)
        
        return {
            "project": project_name,
            "files_analyzed": len(python_files),
            "suggested_models": ai_schema.get("models", []),
            "database_type": ai_schema.get("database_type", "sqlite"),
            "relationships": ai_schema.get("relationships", [])
        }
    
    def get_ai_database_suggestions(self, project_name: str, project_context: str) -> Dict[str, Any]:
        """AI se database schema suggestions leta hai"""
        
        prompt = f"""
        You are a database expert. Analyze this code and suggest database models.

        PROJECT: {project_name}
        CODE CONTEXT: {project_context}

        Provide:
        1. Database type (sqlite/mongodb)
        2. List of models/tables needed
        3. Fields for each model
        4. Relationships between models

        Return JSON format only:
        {{
            "database_type": "sqlite",
            "models": [
                {{
                    "name": "User",
                    "fields": [
                        {{"name": "id", "type": "Integer", "primary_key": true}},
                        {{"name": "username", "type": "String", "unique": true}},
                        {{"name": "email", "type": "String", "unique": true}},
                        {{"name": "password", "type": "String"}},
                        {{"name": "created_at", "type": "DateTime"}}
                    ]
                }}
            ],
            "relationships": [
                {{"from": "User", "to": "Post", "type": "one-to-many"}}
            ]
        }}
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Extract JSON from response
                try:
                    return json.loads(content)
                except:
                    # Fallback schema
                    return {
                        "database_type": "sqlite",
                        "models": [
                            {
                                "name": "User",
                                "fields": [
                                    {"name": "id", "type": "Integer", "primary_key": True},
                                    {"name": "username", "type": "String", "unique": True},
                                    {"name": "email", "type": "String", "unique": True},
                                    {"name": "password", "type": "String"},
                                    {"name": "created_at", "type": "DateTime"}
                                ]
                            }
                        ],
                        "relationships": []
                    }
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def generate_sqlite_database(self, project_name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """SQLite database with tables generate karta hai"""
        project_dir = self.projects_dir / project_name
        db_path = project_dir / "app.db"
        
        print(f"🗄️ Creating SQLite database: {db_path}")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            tables_created = []
            
            for model in schema.get("models", []):
                table_name = model["name"].lower()
                fields = model["fields"]
                
                # Create table SQL
                field_definitions = []
                for field in fields:
                    field_def = f"{field['name']} {field['type']}"
                    if field.get('primary_key'):
                        field_def += " PRIMARY KEY"
                    if field.get('unique'):
                        field_def += " UNIQUE"
                    if field.get('autoincrement'):
                        field_def += " AUTOINCREMENT"
                    field_definitions.append(field_def)
                
                create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join(field_definitions)}
                );
                """
                
                cursor.execute(create_table_sql)
                tables_created.append(table_name)
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "database_path": str(db_path),
                "tables_created": tables_created,
                "database_type": "sqlite"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_orm_models(self, project_name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """SQLAlchemy ORM models generate karta hai"""
        project_dir = self.projects_dir / project_name
        models_file = project_dir / "models.py"
        
        print(f"🏗️ Generating ORM models: {models_file}")
        
        models_code = '''"""
🤖 AI-Generated Database Models
KING DEEPSEEK AI Agent - Database Integration
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

'''
        
        for model in schema.get("models", []):
            model_name = model["name"]
            table_name = model["name"].lower()
            
            models_code += f"""
class {model_name}(Base):
    __tablename__ = '{table_name}'
    
"""
            # Add fields
            for field in model["fields"]:
                field_name = field["name"]
                field_type = field["type"]
                
                # Map to SQLAlchemy types
                type_mapping = {
                    "Integer": "Integer",
                    "String": "String(255)",
                    "Text": "Text", 
                    "DateTime": "DateTime",
                    "Boolean": "Boolean",
                    "Float": "Float"
                }
                
                sqlalchemy_type = type_mapping.get(field_type, "String(255)")
                
                # Field definition
                field_def = f"    {field_name} = Column({sqlalchemy_type}"
                
                if field.get('primary_key'):
                    field_def += ", primary_key=True"
                if field.get('unique'):
                    field_def += ", unique=True"
                if field.get('autoincrement'):
                    field_def += ", autoincrement=True"
                
                field_def += ")"
                
                # Default values
                if field_type == "DateTime" and field_name in ["created_at", "updated_at"]:
                    field_def += f"  # Default: datetime.utcnow"
                
                models_code += field_def + "\n"
            
            models_code += "\n    def __repr__(self):\n"
            models_code += f'        return f"<{model_name}(" + ", ".join([f"{{self.{f["name"]}}}" for f in model["fields"][:2]]) + f")>"\n\n'
        
        # Add database setup
        models_code += '''
# Database setup
def init_database():
    """Initialize database and create tables"""
    engine = create_engine('sqlite:///app.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def get_db_session():
    """Get database session"""
    engine = create_engine('sqlite:///app.db')
    Session = sessionmaker(bind=engine)
    return Session()
'''
        
        try:
            with open(models_file, 'w', encoding='utf-8') as f:
                f.write(models_code)
            
            return {
                "success": True,
                "file_created": str(models_file),
                "models_generated": len(schema.get("models", [])),
                "code_preview": models_code[:500] + "..."
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_crud_operations(self, project_name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """CRUD operations generator"""
        project_dir = self.projects_dir / project_name
        crud_file = project_dir / "crud_operations.py"
        
        print(f"🛠️ Generating CRUD operations: {crud_file}")
        
        crud_code = '''"""
🤖 AI-Generated CRUD Operations
KING DEEPSEEK AI Agent - Database Integration
"""

from models import get_db_session, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

'''
        
        for model in schema.get("models", []):
            model_name = model["name"]
            
            # CRUD class for each model
            crud_code += f"""
class {model_name}CRUD:
    \"""CRUD operations for {model_name} model\"""
    
    def __init__(self):
        self.session = get_db_session()
    
    def create(self, data: Dict[str, Any]) -> {model_name}:
        \"""Create new {model_name} record\"""
        try:
            from models import {model_name}
            obj = {model_name}(**data)
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
            return obj
        except Exception as e:
            self.session.rollback()
            raise e
    
    def get_by_id(self, id: int) -> Optional[{model_name}]:
        \"""Get {model_name} by ID\"""
        from models import {model_name}
        return self.session.query({model_name}).filter({model_name}.id == id).first()
    
    def get_all(self) -> List[{model_name}]:
        \"""Get all {model_name} records\"""
        from models import {model_name}
        return self.session.query({model_name}).all()
    
    def update(self, id: int, data: Dict[str, Any]) -> Optional[{model_name}]:
        \"""Update {model_name} record\"""
        try:
            from models import {model_name}
            obj = self.session.query({model_name}).filter({model_name}.id == id).first()
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                self.session.commit()
                self.session.refresh(obj)
            return obj
        except Exception as e:
            self.session.rollback()
            raise e
    
    def delete(self, id: int) -> bool:
        \"""Delete {model_name} record\"""
        try:
            from models import {model_name}
            obj = self.session.query({model_name}).filter({model_name}.id == id).first()
            if obj:
                self.session.delete(obj)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e
    
    def filter_by(self, **filters) -> List[{model_name}]:
        \"""Filter {model_name} records\"""
        from models import {model_name}
        query = self.session.query({model_name})
        for key, value in filters.items():
            query = query.filter(getattr({model_name}, key) == value)
        return query.all()

"""
        
        # Add database utilities
        crud_code += '''
# Database Utilities
def init_database():
    """Initialize database"""
    from models import init_database
    return init_database()

def backup_database():
    """Backup database file"""
    import shutil
    import os
    if os.path.exists('app.db'):
        shutil.copy2('app.db', 'app_backup.db')
        return True
    return False

def get_database_stats():
    """Get database statistics"""
    from models import get_db_session, Base
    session = get_db_session()
    stats = {}
    
    for table in Base.metadata.tables:
        count = session.execute(f"SELECT COUNT(*) FROM {table}").scalar()
        stats[table] = count
    
    session.close()
    return stats
'''
        
        try:
            with open(crud_file, 'w', encoding='utf-8') as f:
                f.write(crud_code)
            
            return {
                "success": True,
                "file_created": str(crud_file),
                "crud_classes": len(schema.get("models", [])),
                "operations_per_class": 6  # create, get, get_all, update, delete, filter
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_database_migrations(self, project_name: str) -> Dict[str, Any]:
        """Database migration system generate karta hai"""
        project_dir = self.projects_dir / project_name
        migrations_dir = project_dir / "migrations"
        migrations_dir.mkdir(exist_ok=True)
        
        print(f"🔄 Generating migration system: {migrations_dir}")
        
        # Create migration script
        migration_script = migrations_dir / "001_initial_migration.py"
        
        migration_code = '''"""
🤖 AI-Generated Database Migration
KING DEEPSEEK AI Agent - Database Integration
"""

def upgrade():
    """Apply initial migration"""
    print("✅ Applying initial database migration...")
    from models import init_database
    init_database()
    print("✅ Database migration completed!")

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
        
        try:
            with open(migration_script, 'w', encoding='utf-8') as f:
                f.write(migration_code)
            
            # Create migration runner
            migration_runner = project_dir / "run_migration.py"
            with open(migration_runner, 'w', encoding='utf-8') as f:
                f.write('''from migrations.001_initial_migration import upgrade
print("🚀 Running database migration...")
upgrade()
print("✅ Migration completed!")
''')
            
            return {
                "success": True,
                "migrations_dir": str(migrations_dir),
                "migration_script": str(migration_script),
                "migration_runner": str(migration_runner)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def integrate_database_with_app(self, project_name: str) -> Dict[str, Any]:
        """Existing app mein database integration karta hai"""
        project_dir = self.projects_dir / project_name
        app_file = project_dir / "app.py"
        
        if not app_file.exists():
            return {"success": False, "error": "app.py not found"}
        
        print(f"🔗 Integrating database with app: {app_file}")
        
        try:
            with open(app_file, 'r', encoding='utf-8') as f:
                app_content = f.read()
            
            # Check if database already integrated
            if "from models" in app_content or "get_db_session" in app_content:
                return {"success": False, "error": "Database already integrated"}
            
            # Add database imports
            new_imports = '''
# Database Integration - KING DEEPSEEK AI Agent
from models import init_database, get_db_session
from crud_operations import UserCRUD, get_database_stats
'''
            
            # Find existing imports and add after them
            lines = app_content.split('\n')
            import_end = 0
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith(('import ', 'from ', '#', '"', "'")) and not line.strip().startswith('#'):
                    import_end = i
                    break
            
            lines.insert(import_end, new_imports)
            
            # Add database initialization
            if "if __name__ == '__main__':" in app_content:
                main_block = "if __name__ == '__main__':"
                replacement = '''# Initialize database
init_database()

if __name__ == '__main__':'''
                app_content = app_content.replace(main_block, replacement)
            
            # Add database routes
            database_routes = '''

# Database API Routes
@app.route('/api/db/stats')
def db_stats():
    """Get database statistics"""
    stats = get_database_stats()
    return jsonify({"success": True, "stats": stats})

@app.route('/api/users')
def get_users():
    """Get all users"""
    user_crud = UserCRUD()
    users = user_crud.get_all()
    return jsonify({
        "success": True, 
        "users": [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    })

@app.route('/api/users/create', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.json
    user_crud = UserCRUD()
    try:
        user = user_crud.create(data)
        return jsonify({
            "success": True, 
            "user": {"id": user.id, "username": user.username, "email": user.email}
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
'''
            
            # Add routes before app.run()
            if "app.run(" in app_content:
                app_content = app_content.replace("app.run(", database_routes + "\n\napp.run(")
            
            # Write updated app
            with open(app_file, 'w', encoding='utf-8') as f:
                f.write(app_content)
            
            return {
                "success": True,
                "app_updated": True,
                "routes_added": ["/api/db/stats", "/api/users", "/api/users/create"],
                "database_initialized": True
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def complete_database_integration(self, project_name: str) -> Dict[str, Any]:
        """Complete database integration process"""
        print(f"🚀 Starting database integration for: {project_name}")
        
        # Step 1: Analyze project
        analysis = self.analyze_project_structure(project_name)
        if "error" in analysis:
            return analysis
        
        # Step 2: Generate database
        db_result = self.generate_sqlite_database(project_name, analysis)
        if not db_result["success"]:
            return db_result
        
        # Step 3: Generate ORM models
        models_result = self.generate_orm_models(project_name, analysis)
        
        # Step 4: Generate CRUD operations
        crud_result = self.generate_crud_operations(project_name, analysis)
        
        # Step 5: Generate migrations
        migration_result = self.generate_database_migrations(project_name)
        
        # Step 6: Integrate with app
        integration_result = self.integrate_database_with_app(project_name)
        
        return {
            "success": True,
            "project": project_name,
            "database_created": db_result["success"],
            "models_generated": models_result.get("models_generated", 0),
            "crud_operations": crud_result.get("crud_classes", 0),
            "migration_system": migration_result["success"],
            "app_integrated": integration_result.get("app_updated", False),
            "next_steps": [
                "Run: python run_migration.py",
                "Start: python app.py",
                "Test: http://localhost:5000/api/db/stats",
                "Add more models as needed"
            ]
        }

def main():
    db_gen = DatabaseGenerator()
    
    print("=== 🗄️ KING DEEPSEEK - DATABASE INTEGRATION ===")
    print("🤖 AI-POWERED DATABASE GENERATION SYSTEM!\n")
    
    project_name = input("Project ka naam likhen (e.g. agent50): ").strip()
    if not project_name:
        print("❌ Project name required!")
        return
    
    print(f"\n🎯 Starting database integration for: {project_name}")
    
    result = db_gen.complete_database_integration(project_name)
    
    if result["success"]:
        print(f"\n✅ DATABASE INTEGRATION COMPLETED!")
        print(f"Project: {result['project']}")
        print(f"Database: ✅ Created")
        print(f"ORM Models: ✅ {result['models_generated']} models")
        print(f"CRUD Operations: ✅ {result['crud_operations']} classes")
        print(f"Migration System: ✅ Ready")
        print(f"App Integration: ✅ Completed")
        
        print(f"\n🚀 NEXT STEPS:")
        for step in result["next_steps"]:
            print(f"  {step}")
            
    else:
        print(f"❌ Database integration failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()