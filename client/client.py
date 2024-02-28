import requests


response = requests.post(
    'http://localhost:8080/auth',
    json={
        "email":"salmansyyd@salman.com",
        "password": "weakpassword"
    },
)

print(response.text)