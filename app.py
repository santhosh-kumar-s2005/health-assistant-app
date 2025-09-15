import streamlit as st
from claude_model import ask_ai
import hashlib
import uuid
from datetime import datetime
from storage import save_conversation

st.set_page_config(page_title="Health Assistant Pro", page_icon="🏥", layout="wide")

# =================== HIGH CONTRAST CSS ===================
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f9f9f9 0%, #e3f2fd 100%);
        font-family: 'Segoe UI', sans-serif;
        color: #232323;
        font-size: 19px;
    }
    .stChatMessage {
        padding: 22px 27px;
        border-radius: 18px;
        margin: 14px 0;
        max-width: 90%;
        font-size: 1.15em;
        line-height: 2.1;
    }
    /* User messages: pure white text, vivid blue bubble */
    [data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, #0a2963, #1976d2);
        color: #ffffff !important;
        font-weight: 700;
        font-size: 1.25em;
        letter-spacing: 0.03em;
        margin-left: auto;
        box-shadow: 0px 2px 6px rgba(30, 87, 153, 0.15);
    }
    /* Assistant messages: black text, white bubble, blue border */
    [data-testid="stChatMessageAssistant"] {
        background: #ffffff;
        color: #000000 !important; /* Changed to pure black */
        border: 2px solid #1976d2;
        font-size: 1.18em;
        box-shadow: 0px 2px 6px rgba(21, 101, 192, 0.09);
        margin-right: auto;
    }
    [data-testid="stChatMessageAssistant"] p {
        font-size: 1.19em;
        line-height: 2.2;
        color: #000000 !important; /* Changed to pure black */
        word-break: break-word;
        font-weight: 600;
    }
    [data-testid="stChatMessageAssistant"] strong {
        color: #1565c0;
        font-weight: 900;
    }
    [data-testid="stChatMessageAssistant"] em {
        color: #b71c1c;
        font-style: italic;
        font-weight: 700;
    }
    [data-testid="stChatMessageAssistant"] ul {
        margin: 14px 0;
        padding-left: 25px;
        font-size: 1.15em;
        color: #000000 !important; /* Changed to pure black */
    }
    .stTextInput > div > div > input {
        border-radius: 30px;
        padding: 16px 18px;
        border: 2px solid #1565c0;
        font-size: 1.14em;
        background: #f5faff;
        color: #222222;
        font-weight: 700;
    }
    button {
        font-size: 1.13em !important;
        background: #1976d2 !important;
        color: #fff !important;
        padding: 10px 22px !important;
        border-radius: 22px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0px 2px 6px rgba(21, 101, 192, 0.11);
    }
    button:hover {
        background: #1565c0 !important;
        color: #fff !important;
    }
    .privacy-badge {
        background: #e3f2fd;
        padding: 12px 19px;
        border-radius: 15px;
        font-size: 1.1em;
        font-weight: 700;
        color: #0d47a1;
        display: inline-block;
        margin: 8px 0;
        letter-spacing: 0.01em;
        box-shadow: 0px 1px 5px rgba(21, 101, 192, 0.07);
    }
    h1 {
        font-size: 2.4em !important;
        color: #174ea6 !important;
        font-weight: 900;
        letter-spacing: 0.02em;
        text-align: center;
        margin-bottom: 0.4em;
    }
    .desc-text {
        text-align: center;
        color: #3b3b3b;
        font-size: 1.22em;
        margin-bottom: 10px;
        font-weight: 500;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# =================== SECURITY FUNCTIONS ===================
def get_anonymous_user_id():
    """Generate secure anonymous user ID without affecting UI"""
    if 'anonymous_id' not in st.session_state:
        session_data = f"{uuid.uuid4()}{datetime.now().timestamp()}"
        st.session_state.anonymous_id = hashlib.sha256(session_data.encode()).hexdigest()
    return st.session_state.anonymous_id

def sanitize_input(user_input):
    """Basic input sanitization that doesn't change visible text"""
    if not user_input:
        return ""
    sanitized = user_input.replace('<', '').replace('>', '')
    return sanitized[:500]

# =================== HEADER ===================
st.title("🏥 Health Assistant Pro")
st.markdown('<p class="desc-text">Your friendly AI health guide. Ask me about fitness, diet, or wellness tips 👇</p>', unsafe_allow_html=True)
st.markdown('<div class="privacy-badge">🔒 Secure & Private Chat</div>', unsafe_allow_html=True)

# =================== CHAT STATE ===================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# =================== CHAT INPUT HANDLER ===================
if prompt := st.chat_input("💬 Type your health question..."):
    sanitized_prompt = sanitize_input(prompt)
    user_id = get_anonymous_user_id()
    timestamp = datetime.now().isoformat()
    
    # Display user message (original text)
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "user_id": user_id,
        "timestamp": timestamp
    })
    save_conversation(user_id, "user", prompt, timestamp)
    
    # Get AI response
    response = ask_ai(sanitized_prompt)
    styled_response = f"""
    <div style='line-height: 1.9; color: white; font-size: 1.15em;'>
        <p style='margin-bottom: 15px;'>{response}</p>
        <div style='background: black; padding: 14px; border-radius: 12px; margin: 12px 0; border-left: 4px solid #1565c0; font-size: 1.05em;'>
            <span style='color:red; font-weight: bold;'>💡 Pro Tip:</span> Always consult a doctor for serious health concerns.
        </div>
    </div>
    """
    with st.chat_message("assistant"):
        st.markdown(styled_response, unsafe_allow_html=True)
    st.session_state.messages.append({
        "role": "assistant", 
        "content": styled_response,
        "user_id": user_id,
        "timestamp": timestamp
    })
    save_conversation(user_id, "assistant", response, timestamp)