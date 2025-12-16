import sys
import time
import requests
import subprocess
import json
import os
from pathlib import Path
from agent_config import get_project_path

def run_qa_checks(project_name):
    print(f"DOCTOR: Diagnosing {project_name}...")
    
    project_dir = get_project_path(project_name)
    app_file = project_dir / "app.py"
    report_file = project_dir / "qa_report.json"
    
    print("  [START] Starting Flask Server for Testing...")
    
    # Start process
    process = subprocess.Popen(
        [sys.executable, str(app_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(project_dir)
    )

    # Wait for server
    server_ready = False
    for i in range(10):  # 10 seconds
        time.sleep(1)
        try:
            r = requests.get("http://127.0.0.1:5000/", timeout=2)
            if r.status_code < 500:
                server_ready = True
                print(f"  [OK] Server ready after {i+1} seconds")
                break
        except:
            continue
    
    if not server_ready:
        process.terminate()
        print("  [ERROR] Server timeout")
        report = {"status": "CRASH", "error_type": "SERVER_TIMEOUT"}
        with open(report_file, "w") as f: 
            json.dump(report, f)
        sys.exit(1)
    
    print("  [OK] Server alive. Testing endpoints...")
    
    failures = []
    api_url = "http://127.0.0.1:5000"
    
    # Test 1: Root endpoint
    try:
        r = requests.get(api_url, timeout=5)
        if r.status_code != 200:
            failures.append(f"GET / returned {r.status_code}")
        else:
            print(f"    [PASS] GET / - {r.status_code}")
    except Exception as e:
        failures.append(f"GET / error: {e}")
    
    # Test 2: GET /login
    try:
        r = requests.get(f"{api_url}/login", timeout=5)
        if r.status_code not in [200, 302, 405]:
            failures.append(f"GET /login status: {r.status_code}")
        else:
            print(f"    [PASS] GET /login - {r.status_code}")
    except Exception as e:
        failures.append(f"GET /login error: {e}")
    
    # Test 3: POST /login
    try:
        test_data = {"username": "test", "email": "test@test.com"}
        r = requests.post(f"{api_url}/login", json=test_data, timeout=5)
        if r.status_code >= 500:
            failures.append(f"POST /login server error: {r.status_code}")
        else:
            print(f"    [PASS] POST /login - {r.status_code}")
    except Exception as e:
        failures.append(f"POST /login error: {e}")
    
    # Cleanup
    process.terminate()
    time.sleep(1)
    
    # Final decision
    if failures:
        print(f"  [WARN] Issues: {len(failures)}")
        report = {
            "status": "FUNCTIONAL_FAIL", 
            "error_type": "LOGIC_ERROR", 
            "broken_file": "routes.py", 
            "failures": failures
        }
        with open(report_file, "w") as f: 
            json.dump(report, f)
        sys.exit(1)
    else:
        print("  [PASS] All tests passed!")
        report = {"status": "PASSED"}
        with open(report_file, "w") as f: 
            json.dump(report, f)
        sys.exit(0)

# Main block - SIMPLIFIED to avoid line 301 error
if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Error: Project name required")
        sys.exit(1)
    
    project_name = sys.argv[1]
    run_qa_checks(project_name)