import streamlit as st
import requests
import random
import string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


def create_user(username, password):
    login_url = "https://app.eoesonic.com/auth/login"
    login_data = {
        "username": 'admin_user',
        "password": 'admin_pass'
    }

    login_response = requests.post(login_url, json=login_data, verify=False)
    login_response_json = login_response.json()

    token = login_response_json.get("token")

    if token:
        create_user_url = "https://app.eoesonic.com/api/user"
        headers = {
            "x-nd-authorization": f"Bearer {token}"
        }
        user_data = {
            "isAdmin": False,
            "userName": username,
            "name": generate_random_string(12),  # 任意の12文字
            "password": password
        }
        create_user_response = requests.post(create_user_url, headers=headers, json=user_data, verify=False)
        create_user_response_json = create_user_response.json()

        return create_user_response_json
    return None


st.title("EOESonic 用户注册")


with st.form("my_form"):
    username = st.text_input('用户名')
    password = st.text_input('密码', type='password')
    
    submitted = st.form_submit_button("确认")
    if submitted:
        create_user_response_json = create_user(username, password)
        if "id" in create_user_response_json:
            st.success("OK.")
        else:
            st.error("Not OK.")
        st.json(create_user_response_json)


st.markdown('[主页](https://eoesonic.com)')
