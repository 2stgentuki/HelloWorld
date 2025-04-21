import requests
import streamlit as st

dify_api_key = st.secrets["dify"]["api_key"]
url = 'https://api.dify.ai/v1/chat-messages'

# 認証情報の設定
CORRECT_ID = "ru-to"
CORRECT_PASSWORD = "pasuwa-do"

# カスタムCSSでデザインを強化
st.markdown("""
    <style>
    /* 全体のフォントと背景 */
    body {
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: #ffffff;
    }
    /* タイトル */
    h1 {
        font-size: 2.5em;
        text-align: center;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    /* ログイン画面の説明文 */
    .stMarkdown p {
        color: #ffffff;
    }
    /* 入力フォーム */
    .stTextInput > div > input {
        background-color: #ffffff;
        color: #333;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #ccc;
    }
    /* ボタン */
.stButton > button {
    background-color: #ffffff !important;  /* 背景を白に */
    color: #000000 !important;             /* 🔽 テキストを黒に */
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background-color: #e0e0e0 !important;  /* ホバー時はグレー */
    color: #000000 !important;             /* テキスト黒のまま */
    transform: scale(1.05);
}

    /* チャットメッセージ */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    /* チャット入力 */
    .stChatInput > div > input {
        background-color: #ffffff;
        color: #333;
        border-radius: 20px;
        padding: 10px;
    }
    /* エラーメッセージ */
    .stError {
        background-color: #ff4d4d;
        color: white;
        border-radius: 5px;
        padding: 10px;
    }
    /* ライトテーマ用の調整 */
    @media (prefers-color-scheme: light) {
        h1, .stMarkdown p {
            color: #ffffff !important;
        }
    }
        /* フォーム送信ボタンの強制上書き */
    form button {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-weight: bold;
        border: 2px solid #000000 !important;
        border-radius: 8px;
    }
    form button:hover {
        background-color: #f0f0f0 !important;
    }

    </style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# 認証フォーム
def authenticate():
    st.title("🔐 ロボ角川のお悩み相談室 - ログイン")
    st.markdown("**IDとパスワードを入力してログインしてください**")
    
    with st.form("login_form"):
        user_id = st.text_input("ID", placeholder="IDを入力")
        password = st.text_input("パスワード", type="password", placeholder="パスワードを入力")
        submit_button = st.form_submit_button("ログイン")
        
        if submit_button:
            if user_id == CORRECT_ID and password == CORRECT_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("IDまたはパスワードが間違っています。")

# メインのチャット画面
def main_app():
    st.title('🤖 ロボ角川のお悩み相談室')
    st.markdown("****")

    # チャット履歴の表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])

    prompt = st.chat_input("なんでも聞いてよ( ･´ｰ･｀)", key="chat_input")

    if prompt:
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            message_placeholder.markdown("💬 考え中...")  # ローディング表示

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
                full_response = "⚠️ エラーが発生しました。もう一度試してください。"

            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# 認証状態に応じて表示を切り替え
if not st.session_state.authenticated:
    authenticate()
else:
    main_app()
