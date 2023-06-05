import requests
import json


url = "https://app.eoesonic.com/auth/login"

data = {
    "username": "admin_user",
    "password": "admin_pass"
}

# JSONデータをリクエストボディに変換
payload = json.dumps(data)

# POSTリクエストを送信
response = requests.post(url, data=payload, verify=False)

# レスポンスを表示
print(response.text)
