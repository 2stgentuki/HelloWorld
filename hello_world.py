# カスタムCSSを修正
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
        color: #000000; /* 明るい背景でも見えるように黒に変更 */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    /* ログイン画面の説明文 */
    .stMarkdown p {
        color: #000000; /* 説明文も黒で読みやすく */
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
        background-color: #ff6f61;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #e55a50;
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
            color: #000000; /* ライトモードでテキストを黒に */
        }
    }
    </style>
""", unsafe_allow_html=True)
