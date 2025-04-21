import requests
import streamlit as st

# Apply theme-aware styles
st.markdown(
    """
    <style>
    .stApp {
        background-color: var(--background-color, #f8f9fa);
        color: var(--text-color, #212529);
    }
    .stMarkdown, .stTextInput, .stButton, .stChatInput, .stChatMessage, .stTitle {
        color: inherit !important;
    }

    /* チャット入力欄の強調（テーマに合わせて調整） */
    section[data-testid="stChatInput"] {
        background-color: rgba(240, 240, 240, 0.95);
        border: 2px solid #888;
        border-radius: 10px;
        padding: 12px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
    }
    section[data-testid="stChatInput"] input {
        background-color: #fff;
        color: #000;
        border-radius: 8px;
        border: 1px solid #ccc;
    }
    section[data-testid="stChatInput"] button {
        background-color: #007bff;
        color: #fff;
        border: none;
    }
    section[data-testid="stChatInput"] button:hover {
        background-color: #0056b3;
    }

    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #000000;
            color: #FFFFFF;
        }
        section[data-testid="stChatInput"] {
            background-color: #111111 !important;
            border: 2px solid #555 !important;
        }
        section[data-testid="stChatInput"] input {
            background-color: #222222 !important;
            color: #ffffff !important;
            border: 1px solid #666 !important;
        }
        section[data-testid="stChatInput"] button {
            background-color: #333 !important;
            color: #fff !important;
            border: 1px solid #666 !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dify API settings
url = 'https://api.dify.ai/v1/chat-messages'
dify_api_key = st.secrets["dify"]["api_key"]

# Authentication credentials
CORRECT_ID = "ru-to"
CORRECT_PASSWORD = "pasuwa-do"

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# Authentication form
def authenticate():
    st.title("🔐 ロボ角川のお悩み相談室")
    st.markdown("**IDとパスワードを入力してログインしてください**")

    user_id = st.text_input("ID", placeholder="IDを入力")
    password = st.text_input("パスワード", type="password", placeholder="パスワードを入力")
    if st.button("ログイン"):
        if user_id == CORRECT_ID and password == CORRECT_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("IDまたはパスワードが間違っています。")

# Main chat application
def main_app():
    st.title('🤖 ロボ角川のお悩み相談室')

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    # Clear divider and chat input
    prompt = st.chat_input("ここにメッセージを入力してください…", key="chat_input")

    # Handle new user message
    # Handle new user message
if prompt:
    # 表示処理を追加
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("💬 考え中...")

        # Send request to Dify
        headers = { 'Authorization': f'Bearer {dify_api_key}', 'Content-Type': 'application/json' }
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
            data = response.json()
            answer = data.get("answer", "レスポンスがありません。")
            st.session_state.conversation_id = data.get("conversation_id", st.session_state.conversation_id)
        except requests.exceptions.RequestException:
            answer = "⚠️ エラーが発生しました。もう一度試してください。"
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# Application entry point
if not st.session_state.authenticated:
    authenticate()
else:
    main_app()
