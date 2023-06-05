import streamlit as st
import requests


def create_user(username, password):
    # ログイン用のURLとデータ
    login_url = "https://app.eoesonic.com/auth/login"
    login_data = {
        "username": 'admin_user',
        "password": 'admin_pass'
    }

    # ログインリクエストを送信
    login_response = requests.post(login_url, json=login_data, verify=False)
    login_response_json = login_response.json()

    # トークンを取得
    token = login_response_json.get("token")

    if token:
        # ユーザー作成用のURLとデータ
        create_user_url = "https://app.eoesonic.com/api/user"
        headers = {
            "x-nd-authorization": f"Bearer {token}"
        }
        user_data = {
            "isAdmin": False,
            "userName": username,
            "name": "Random8",  # 任意の8文字
            "password": password
        }

        # ユーザー作成リクエストを送信
        create_user_response = requests.post(create_user_url, headers=headers, json=user_data, verify=False)
        create_user_response_json = create_user_response.json()

        # レスポンスを返す
        return create_user_response_json

    # トークンが取得できなかった場合はNoneを返す
    return None


st.title("create user")


with st.form("my_form"):
    username = st.text_input('username')
    password = st.text_input('password', type='password')
    
    st.write("Inside the form")
    submitted = st.form_submit_button("Submit")
    if submitted:
        create_user_response_json = create_user(username, password)
        st.json(create_user_response_json)


st.write("Outside the form")
st.markdown('[homepage](https://eoesonic.com)')