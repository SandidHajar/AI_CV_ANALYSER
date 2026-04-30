import requests

with open('dummy.pdf', 'wb') as f:
    f.write(b'dummy content')

with open('dummy.pdf', 'rb') as f:
    r = requests.post('http://localhost:8000/extract-text', files={'file': ('dummy.pdf', f, 'application/pdf')})

print(r.status_code)
print(r.text)
