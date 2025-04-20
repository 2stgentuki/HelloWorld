import requests
import streamlit as st

dify_api_key = st.secrets["dify"]["api_key"]
url = 'https://api.dify.ai/v1/chat-messages'

# 認証情報の設定
CORRECT_ID = "ru-to"
CORRECT_PASSWORD = "pasuwa-do"

# セッション状態の初期化
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# 認証フォーム
def authenticate():
    st.title("ログイン")
    user_id = st.text_input("ID", key="user_id")
    password = st.text_input("パスワード", type="password", key="password")
    if st.button("ログイン"):
        if user_id == CORRECT_ID and password == CORRECT_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()  # 画面を更新
        else:
            st.error("IDまたはパスワードが間違っています。")

# メインのチャット画面
def main_app():
    st.title('ロボ川のお悩み相談室')

    # チャット履歴の表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("なんでも聞いてよ")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("...")  # ローディング表示

            headers = {
                'Authorization': f'Bearer {dify_api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                "inputs": {},
                "query": prompt,
                "response_mode": "blocking",
                "conversation_id": st.session_state.conversation_id,
                "user": "alex-123",
                "files": []
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                response_data = response.json()

                full_response = response_data.get("answer", "レスポンスがありません。")
                new_conversation_id = response_data.get("conversation_id", st.session_state.conversation_id)

                st.session_state.conversation_id = new_conversation_id

            except requests.exceptions.RequestException:
                full_response = "エラーが発生しました。もう一度試してください。"

            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# 認証状態に応じて表示を切り替え
if not st.session_state.authenticated:
    authenticate()
else:
    main_app()
