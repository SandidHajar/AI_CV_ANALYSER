import urllib.request
import urllib.error
import json

req = urllib.request.Request(
    'https://ai-cv-analyser-zus6.vercel.app/_/backend/auth/login', 
    data=json.dumps({'email':'test@test.com','password':'test'}).encode(), 
    headers={'Content-Type': 'application/json'}
)

try:
    urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
    print(e.read().decode())
