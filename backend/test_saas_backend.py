import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_saas_workflow():
    email = f"test_{int(time.time())}@example.com"
    password = "password123"
    
    # 1. Register
    print("--- Registering ---")
    reg_resp = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    print(f"Register: {reg_resp.status_code}, {reg_resp.text}")
    
    # 2. Login
    print("\n--- Logging in ---")
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    print(f"Login: {login_resp.status_code}, {login_resp.text}")
    token = login_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Start Analysis
    print("\n--- Starting Analysis ---")
    data = {"cv_text": "I am a Python developer with experience in FastAPI and React and Docker and SQL."}
    analyze_resp = requests.post(f"{BASE_URL}/analyze-cv", json=data, headers=headers)
    print(f"Analyze Status: {analyze_resp.status_code}")
    job_id = analyze_resp.json().get("job_id")
    print(f"Job ID: {job_id}")
    
    # 4. Poll for status
    print("\n--- Polling for Status ---")
    for _ in range(10):
        status_resp = requests.get(f"{BASE_URL}/analysis-status/{job_id}", headers=headers)
        status_data = status_resp.json()
        print(f"Status: {status_data['status']}")
        if status_data['status'] == 'completed':
            print(f"Result: {status_data['result']}")
            break
        elif status_data['status'] == 'failed':
            print("Job failed!")
            break
        time.sleep(1)

if __name__ == "__main__":
    test_saas_workflow()
