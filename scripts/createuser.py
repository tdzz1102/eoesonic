import requests
import json


url = "https://app.eoesonic.com/api/user"

headers = {
    "x-nd-authorization": f"Bearer your_login_token",
}

data = {
    "isAdmin": False,
    "userName": "adduser",
    "name": "adduser",
    "password": "adduser"
}

payload = json.dumps(data)

response = requests.post(url, headers=headers, data=payload, verify=False)

print(response.text)
