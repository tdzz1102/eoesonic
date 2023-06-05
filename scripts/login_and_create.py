import requests
import sys


def create_user(username, password):
    # login
    login_url = "https://app.eoesonic.com/auth/login"
    login_data = {
        "username": 'admin_user',
        "password": 'admin_pass'
    }
    login_response = requests.post(login_url, json=login_data, verify=False)
    login_response_json = login_response.json()
    token = login_response_json.get("token")

    if token:
        # create user
        create_user_url = "https://app.eoesonic.com/api/user"
        headers = {
            "x-nd-authorization": f"Bearer {token}"
        }
        user_data = {
            "isAdmin": False,
            "userName": username,
            "name": "Random8",  
            "password": password
        }
        create_user_response = requests.post(create_user_url, headers=headers, json=user_data, verify=False)
        create_user_response_json = create_user_response.json()
        return create_user_response_json


if __name__ == "__main__":
    # コマンドライン引数からユーザー名とパスワードを取得
    args = sys.argv[1:]
    if len(args) < 2:
        print("ユーザー名とパスワードを指定してください。")
        sys.exit(1)

    username = args[0]
    password = args[1]

    response = create_user(username, password)
    if response:
        print("ユーザー作成成功")
        print(response)
    else:
        print("トークンの取得に失敗しました")