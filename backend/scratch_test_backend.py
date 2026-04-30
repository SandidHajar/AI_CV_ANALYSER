import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Health Check: {response.status_code}, {response.json()}")
    except Exception as e:
        print(f"Health Check failed: {e}")

def test_analyze():
    try:
        data = {"cv_text": "I am a Python developer with experience in FastAPI and React."}
        response = requests.post(f"{BASE_URL}/analyze-cv", json=data)
        print(f"Analyze CV: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Analyze CV failed: {e}")

if __name__ == "__main__":
    test_health()
    test_analyze()
