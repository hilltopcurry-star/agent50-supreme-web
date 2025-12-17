# deploy_runner.py
import os
import subprocess
import sys
from datetime import datetime

class DeploymentRunner:
    def __init__(self):
        self.deployment_log = []
    
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        self.deployment_log.append(log_message)
        print(log_message)
    
    def run_command(self, command, check=True):
        """Run shell command and log output"""
        self.log(f"Running: {command}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
            self.log(f"Output: {result.stdout}")
            if result.stderr:
                self.log(f"Error: {result.stderr}")
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed: {e}")
            return False
    
    def docker_deploy(self):
        """Deploy using Docker"""
        self.log("Starting Docker deployment...")
        
        # Build Docker image
        if not self.run_command("docker build -t king-deepseek ."):
            return False
        
        # Run with Docker Compose
        if not self.run_command("docker-compose up -d"):
            return False
        
        self.log("✅ Docker deployment completed")
        return True
    
    def cloud_deploy(self, provider="aws"):
        """Deploy to cloud provider"""
        self.log(f"Starting {provider.upper()} deployment...")
        
        if provider == "aws":
            from aws_deploy import deploy_to_aws
            result = deploy_to_aws()
        elif provider == "azure":
            from azure_deploy import deploy_to_azure
            result = deploy_to_azure()
        else:
            self.log(f"❌ Unknown provider: {provider}")
            return False
        
        if result:
            self.log(f"✅ {provider.upper()} deployment completed")
            return True
        return False
    
    def run_load_test(self):
        """Run load testing"""
        self.log("Starting load tests...")
        
        # Install locust for load testing
        self.run_command("pip install locust")
        
        # Create locustfile for testing
        locustfile = """
from locust import HttpUser, task, between

class KINGDeepseekUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def view_features(self):
        self.client.get("/api/advanced/features")
    
    @task(3)
    def upload_file(self):
        files = {"file": ("test.txt", "Hello World", "text/plain")}
        self.client.post("/api/upload", files=files)
    
    @task(2)
    def chat_message(self):
        self.client.post("/api/chat/send", json={
            "message": "Test message",
            "user_id": "load_test_user"
        })
"""
        
        with open("locustfile.py", "w") as f:
            f.write(locustfile)
        
        self.log("Load test setup complete. Run: locust -f locustfile.py")
        return True

def main():
    runner = DeploymentRunner()
    
    print("🚀 KING DEEPSEEK PRODUCTION DEPLOYMENT")
    print("1. Docker Deployment")
    print("2. AWS Deployment") 
    print("3. Azure Deployment")
    print("4. Load Testing")
    
    choice = input("Select deployment option (1-4): ").strip()
    
    if choice == "1":
        runner.docker_deploy()
    elif choice == "2":
        runner.cloud_deploy("aws")
    elif choice == "3":
        runner.cloud_deploy("azure")
    elif choice == "4":
        runner.run_load_test()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()