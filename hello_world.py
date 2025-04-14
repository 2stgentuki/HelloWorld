import requests
import streamlit as st

dify_api_key = st.secrets["dify"]["api_key"]
url = 'https://api.dify.ai/v1/chat-messages'

st.title('ロボ川のお悩み相談室')

# セッション状態の初期化
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

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
