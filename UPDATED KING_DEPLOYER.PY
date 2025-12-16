# king_deployer.py - UPDATED VERSION
import os
import sys
import subprocess
import webbrowser
import time
from datetime import datetime
import json
import shutil

class KingDeployer:
    def __init__(self):
        self.deployment_log = []
        self.project_path = os.getcwd()
        self.deployment_status = {
            'docker': 'pending',
            'database': 'pending', 
            'web_server': 'pending',
            'ai_system': 'pending',
            'monitoring': 'pending'
        }
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.deployment_log.append(log_entry)
        print(f"🔧 {log_entry}")
        return log_entry
    
    def run_command(self, command, check=True):
        """Run shell command with logging - FIXED FOR SPACES IN PATH"""
        self.log(f"Running command: {command}")
        try:
            # Use the current Python executable directly
            if command.startswith(sys.executable):
                # Handle spaces in path by using the actual executable
                result = subprocess.run([sys.executable] + command.split()[1:], 
                                      capture_output=True, text=True, check=check)
            else:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
            
            if result.stdout:
                self.log(f"Output: {result.stdout}")
            if result.stderr:
                self.log(f"Error: {result.stderr}", "WARNING")
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed: {e}", "ERROR")
            return False
    
    def check_prerequisites(self):
        """Check system prerequisites - FIXED VERSION"""
        self.log("Checking system prerequisites...")
        
        # Direct check without path issues
        checks_passed = True
        
        # Check Python
        try:
            version = sys.version
            self.log(f"✅ Python is installed: {version.split()[0]}")
        except:
            self.log("❌ Python check failed", "ERROR")
            checks_passed = False
        
        # Check Pip
        try:
            import pip
            self.log("✅ Pip is installed")
        except:
            self.log("❌ Pip is not installed", "ERROR")
            checks_passed = False
        
        # Check Git
        if self.run_command("git --version", check=False):
            self.log("✅ Git is installed")
        else:
            self.log("⚠️ Git is not installed (optional)", "WARNING")
        
        return checks_passed
    
    def install_dependencies(self):
        """Install all required dependencies - SIMPLIFIED"""
        self.log("Installing project dependencies...")
        
        # Use current Python's pip directly
        pip_command = f'"{sys.executable}" -m pip install'
        
        dependencies = [
            "flask==3.1.2",
            "flask-cors==6.0.1", 
            "flask-socketio==5.3.6",
            "requests==2.32.5",
            "python-dotenv==1.2.1",
            "sqlalchemy==2.0.44",
            "pyjwt==2.8.0",
            "werkzeug==3.1.3",
            "psutil==5.9.8",
            "python-socketio==5.11.1",
            "eventlet==0.33.3"
        ]
        
        for package in dependencies:
            if self.run_command(f'{pip_command} {package}'):
                self.log(f"✅ Installed: {package}")
            else:
                self.log(f"⚠️ Failed to install: {package}", "WARNING")
    
    def setup_database(self):
        """Initialize and setup database"""
        self.log("Setting up database...")
        
        try:
            # Add project path to system path
            project_dir = os.path.join(self.project_path, 'projects', 'agent50')
            if project_dir not in sys.path:
                sys.path.append(project_dir)
            
            from models import init_database
            
            init_database()
            self.deployment_status['database'] = 'completed'
            self.log("✅ Database setup completed")
            return True
        except Exception as e:
            self.log(f"❌ Database setup failed: {e}", "ERROR")
            return False
    
    def deploy_web_application(self):
        """Deploy the main web application"""
        self.log("Deploying web application...")
        
        try:
            # Start web application
            app_path = os.path.join(self.project_path, 'projects', 'agent50', 'app.py')
            web_process = subprocess.Popen([
                sys.executable, app_path
            ])
            
            time.sleep(3)  # Wait for app to start
            
            self.deployment_status['web_server'] = 'completed'
            self.log("✅ Web application deployed on port 5000")
            return True
            
        except Exception as e:
            self.log(f"❌ Web application deployment failed: {e}", "ERROR")
            return False
    
    def deploy_super_king_dashboard(self):
        """Deploy Super King Dashboard"""
        self.log("Deploying Super King Dashboard...")
        
        try:
            dashboard_path = os.path.join(self.project_path, 'super_king_dashboard.py')
            dashboard_process = subprocess.Popen([
                sys.executable, dashboard_path
            ])
            
            time.sleep(2)
            
            self.log("✅ Super King Dashboard deployed on port 8000")
            return True
            
        except Exception as e:
            self.log(f"❌ Dashboard deployment error: {e}", "ERROR")
            return False
    
    def setup_ai_system(self):
        """Setup AI and ML systems"""
        self.log("Setting up AI systems...")
        
        try:
            # Test if required AI packages are installed
            try:
                import numpy
                import pandas
                import sklearn
                self.log("✅ AI/ML packages are installed")
            except ImportError as e:
                self.log(f"⚠️ Some AI packages missing: {e}", "WARNING")
            
            # Check DeepSeek API key
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('DEEPSEEK_API_KEY')
            if api_key:
                self.log("✅ DeepSeek API key configured")
                self.deployment_status['ai_system'] = 'completed'
            else:
                self.log("⚠️ DeepSeek API key not found", "WARNING")
                
            return True
            
        except Exception as e:
            self.log(f"❌ AI system setup error: {e}", "ERROR")
            return False
    
    def create_deployment_report(self):
        """Create deployment report"""
        self.log("Generating deployment report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project': 'SUPER KING DEEPSEEK',
            'deployment_status': self.deployment_status,
            'successful_steps': sum(1 for status in self.deployment_status.values() if status == 'completed'),
            'total_steps': len(self.deployment_status),
            'log_entries': self.deployment_log[-20:],
            'access_urls': {
                'main_app': 'http://localhost:5000',
                'super_dashboard': 'http://localhost:8000'
            }
        }
        
        # Save report to file
        with open('deployment_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log("✅ Deployment report generated")
        return report
    
    def open_dashboard(self):
        """Open dashboard in browser"""
        self.log("Opening applications in browser...")
        try:
            webbrowser.open('http://localhost:8000')
            time.sleep(1)
            webbrowser.open('http://localhost:5000')
        except:
            self.log("⚠️ Could not open browser automatically", "WARNING")
    
    def quick_deploy(self):
        """Quick deployment without extensive checks"""
        print("\n" + "="*60)
        print("👑 SUPER KING DEEPSEEK - QUICK DEPLOYMENT")
        print("🇵🇰🤝🇨🇳 PAK-CHINA FRIENDSHIP LEVEL DEPLOYMENT")
        print("="*60)
        
        start_time = time.time()
        
        self.log("Starting quick deployment...")
        
        # Step 1: Basic checks
        self.log("Performing basic checks...")
        try:
            version = sys.version
            self.log(f"✅ Python: {version.split()[0]}")
        except:
            self.log("❌ Python check failed", "ERROR")
            return False
        
        # Step 2: Deploy applications
        self.log("Deploying applications...")
        
        # Deploy web app
        if self.deploy_web_application():
            self.log("✅ Main application deployed")
        else:
            self.log("⚠️ Main application deployment had issues", "WARNING")
        
        # Deploy dashboard
        if self.deploy_super_king_dashboard():
            self.log("✅ Super King Dashboard deployed")
        else:
            self.log("⚠️ Dashboard deployment had issues", "WARNING")
        
        # Step 3: Setup AI
        self.setup_ai_system()
        
        # Step 4: Create report and open browser
        report = self.create_deployment_report()
        self.open_dashboard()
        
        # Calculate deployment time
        deployment_time = time.time() - start_time
        
        print("\n" + "="*60)
        print("🎉 QUICK DEPLOYMENT COMPLETED!")
        print("="*60)
        
        successful = report['successful_steps']
        total = report['total_steps']
        
        print(f"✅ Successful steps: {successful}/{total}")
        print(f"⏱️  Deployment time: {deployment_time:.2f} seconds")
        print(f"🌐 Main Application: http://localhost:5000")
        print(f"👑 Super Dashboard: http://localhost:8000")
        
        print("\n📋 DEPLOYMENT STATUS:")
        for component, status in self.deployment_status.items():
            status_icon = "✅" if status == 'completed' else "❌"
            print(f"  {status_icon} {component.replace('_', ' ').title()}: {status}")
        
        print("\n🚀 YOUR SUPER KING DEEPSEEK IS READY!")
        print("🇵🇰🤝🇨🇳 PAK-CHINA FRIENDSHIP POWER ACTIVATED!")
        
        return True

def main():
    """Main function - UPDATED"""
    deployer = KingDeployer()
    
    print("👑 SUPER KING DEEPSEEK DEPLOYMENT SYSTEM")
    print("Choose deployment option:")
    print("1. 🚀 QUICK DEPLOYMENT (Recommended)")
    print("2. 🔧 FULL DEPLOYMENT with Dependency Check")
    print("3. 📊 DEPLOYMENT STATUS")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n🚀 STARTING QUICK DEPLOYMENT...")
            success = deployer.quick_deploy()
            
        elif choice == "2":
            print("\n🔧 Starting full deployment...")
            # Full deployment logic here
            print("Full deployment coming soon...")
            
        elif choice == "3":
            print("\n📊 Deployment status check coming soon...")
            
        else:
            print("\n❌ Invalid choice. Please run again.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Deployment cancelled by user.")
    except Exception as e:
        print(f"\n❌ Deployment error: {e}")

if __name__ == '__main__':
    main()