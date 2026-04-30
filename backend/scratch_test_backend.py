import urllib.request
import urllib.error
import json
import uuid

base_url = 'https://ai-cv-analyser-zus6.vercel.app/_/backend'

email = f"test_{uuid.uuid4().hex[:8]}@test.com"

# 0. Register
req0 = urllib.request.Request(
    f'{base_url}/auth/register', 
    data=json.dumps({'email': email, 'password':'test'}).encode(), 
    headers={'Content-Type': 'application/json'}
)
try:
    urllib.request.urlopen(req0)
except urllib.error.HTTPError as e:
    pass

# 1. Login to get token
req = urllib.request.Request(
    f'{base_url}/auth/login', 
    data=json.dumps({'email': email, 'password':'test'}).encode(), 
    headers={'Content-Type': 'application/json'}
)

try:
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode())
    token = data['access_token']
except urllib.error.HTTPError as e:
    print("Login failed:", e.read().decode())
    exit(1)

# 2. Start analysis with weird characters (null byte, etc)
# PDF text extraction often has null bytes \x00
weird_text = "This is a test CV text.\x00 With a null byte."

req2 = urllib.request.Request(
    f'{base_url}/analyze-cv', 
    data=json.dumps({'cv_text': weird_text}).encode(), 
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
)

try:
    res2 = urllib.request.urlopen(req2)
    print("Analysis Response:", res2.read().decode())
except urllib.error.HTTPError as e:
    print("Analyze failed:", e.read().decode())
