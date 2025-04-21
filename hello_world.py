import requests
import streamlit as st
from streamlit_lottie import st_lottie
import json

# シークレットの読み込み
dify_api_key = st.secrets["dify"]["api_key"]
url = 'https://api.dify.ai/v1/chat-messages'

# 定数
CORRECT_ID = "ru-to"
CORRECT_PASSWORD = "pasuwa-do"

# セッション状態の初期化
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# カスタムCSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #f0f4f8, #d9e2ec);
    }
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #e6f3ff;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #ffffff;
        margin-right: 20%;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: scale(1.05);
    }
    .stTextInput>div>input {
        border-radius: 8px;
        border: 1px solid #ced4da;
    }
    </style>
""", unsafe_allow_html=True)

# Lottieアニメーションの読み込み
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# ログイン画面
def authenticate():
    st.title("🔐 ロボ角川のお悩み相談室")
    st.markdown("**IDとパスワードを入力してログイン**")

    # Lottieアニメーション（例: ロボットのアニメーション）
    try:
        lottie_robot = load_lottiefile("robot.json")  # 事前にLottieファイルを用意
        st_lottie(lottie_robot, height=200)
    except FileNotFoundError:
        st.image("https://via.placeholder.com/200", caption="ロボ角川")  # 代替画像

    with st.container():
        user_id = st.text_input("ID", placeholder="IDを入力")
        password = st.text_input("パスワード", type="password", placeholder="パスワードを入力")
        if st.button("ログイン", key="login"):
            if user_id == CORRECT_ID and password == CORRECT_PASSWORD:
                st.session_state.authenticated = True
                st.success("ログイン成功！")
                st.rerun()
            else:
                st.error("IDまたはパスワードが間違っています。")

# メインアプリ
def main_app():
    st.title('🤖 ロボ角川のお悩み相談室')
    st.markdown("**なんでも気軽に相談してね！**")

    # サイドバー
    with st.sidebar:
        st.header("設定")
        if st.button("ログアウト"):
            st.session_state.authenticated = False
            st.session_state.messages = []
            st.session_state.conversation_id = ""
            st.rerun()
        if st.button("会話履歴をクリア"):
            st.session_state.messages = []
            st.session_state.conversation_id = ""
            st.rerun()

    # チャット表示
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(
                    f'<div class="chat-message {"user-message" if message["role"] == "user" else "assistant-message"}">{message["content"]}</div>',
                    unsafe_allow_html=True
                )

    # チャット入力
    prompt = st.chat_input("なんでも聞いてよ( ･´ｰ･｀)", key="chat_input")
    if prompt:
        with chat_container:
            with st.chat_message("user"):
                st.markdown(
                    f'<div class="chat-message user-message">{prompt}</div>',
                    unsafe_allow_html=True
                )
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("💬 考え中..."):
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
                        st.session_state.conversation_id = response_data.get("conversation_id", st.session_state.conversation_id)
                    except requests.exceptions.RequestException as e:
                        full_response = f"⚠️ エラーが発生しました: {str(e)}"

                    message_placeholder.markdown(
                        f'<div class="chat-message assistant-message">{full_response}</div>',
                        unsafe_allow_html=True
                    )
                    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 認証チェック
if not st.session_state.authenticated:
    authenticate()
else:
    main_app()
