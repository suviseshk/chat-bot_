#without animation and mobile optimized
import streamlit as st
from groq import Groq
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="JACSICE Assistant", page_icon="🏛️", layout="centered")

# --- ADVANCED MODERN CSS (WITH MOBILE OPTIMIZATION) ---
st.markdown("""
<style>
    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth entrance animation for intro */
    @keyframes fadeUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .hero-container {
        animation: fadeUp 1s cubic-bezier(0.16, 1, 0.3, 1);
        text-align: center;
        padding-top: 3rem;
        padding-bottom: 2rem;
    }

    /* Premium Modern Typography */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2em;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Modern Glassmorphism Feature Cards */
    .feature-grid {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 3rem;
        margin-bottom: 3rem;
        animation: fadeUp 1.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        width: 30%;
        transition: transform 0.3s ease, background 0.3s ease, border-color 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    .card-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .card-title { color: #e2e8f0; font-weight: 600; font-size: 1rem; margin-bottom: 0.3rem;}
    .card-text { color: #64748b; font-size: 0.85rem; line-height: 1.4;}

    /* Styling the Streamlit Button to look Premium */
    div.stButton > button {
        background: transparent !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        display: block;
        margin: 0 auto;
    }
    
    div.stButton > button:hover {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.15) !important;
        color: #ffffff !important;
        transform: scale(1.02);
    }

    /* Keep the compact images and chat bubbles */
    [data-testid="stChatMessageContent"] img {
        max-width: 300px !important; 
        height: auto;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        margin-top: 10px;
        border: 2px solid #1A2B4C;
    }
    [data-testid="stChatMessage"] {
        background-color: #1E2329;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #1A2B4C;
    }

    /* =========================================
       📱 MOBILE OPTIMIZATION (MEDIA QUERIES)
       ========================================= */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.2rem; /* Shrink massive title */
        }
        .hero-subtitle {
            font-size: 0.95rem;
            padding: 0 15px; /* Add padding so text doesn't touch screen edges */
        }
        .feature-grid {
            flex-direction: column; /* Stack cards vertically instead of horizontally */
            align-items: center;
            gap: 1rem;
        }
        .glass-card {
            width: 90%; /* Cards take up most of the screen width */
            padding: 1.2rem;
        }
        div.stButton > button {
            width: 80% !important; /* Make button wider for fat-finger tapping */
            padding: 0.8rem 2rem !important; 
        }
        [data-testid="stChatMessageContent"] img {
            max-width: 100% !important; /* Images scale to fit mobile chat bubble */
        }
    }
</style>
""", unsafe_allow_html=True)

# --- THE PROFESSIONAL SIDEBAR ---
with st.sidebar:
    st.image("https://www.jacsicoe.in/images/logo.png", use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: #e2e8f0;'>Neural Interface</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 👨‍💻 System Architect")
    st.info("**Your Name Here**\n\nCSE Department (2026)")
    st.markdown("### 🔗 Directory")
    st.markdown("🎓 [JACSICE Portal](https://www.jacsicoe.in)")
    st.markdown("📞 **Admin:** 04639 279906")
    st.markdown("---")
    st.caption("Engine: Smart Retrieval AI")

# --- LOAD THE DATA ---
@st.cache_data
def load_college_data():
    try:
        with open("college_data.json", "r", encoding="utf-8") as f:
            json_text = f.read()
        with open("extra_info.txt", "r", encoding="utf-8") as f:
            extra_text = f.read()
        return json_text + "\n\n" + extra_text
    except FileNotFoundError:
        return "Error: Data files not found."

college_knowledge = load_college_data()

# --- SYSTEM PROMPT ---
system_instruction = f"""
You are the official AI assistant for Jayaraj Annapackiam CSI College of Engineering (JACSICE).
Your goal is to be helpful, professional, and friendly.

RULES:
1. Use the COLLEGE DATA below to answer questions about the college.
2. If the user asks about a topic and there is a Markdown image link (e.g., ![Image Name](url)) next to that topic in the data, you MUST include that exact Markdown image link in your final response!
3. If they ask a general question, answer normally.
4. If they ask about college info NOT in the data, admit you don't know yet. Do not make up facts.

COLLEGE DATA:
{college_knowledge}
"""

# --- CONFIGURE AI (GROQ) ---
# Streamlit will pull this securely from the cloud settings
client = Groq(api_key=st.secrets["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"])

# --- APP ROUTING & STATE ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "intro"

# --- PAGE 1: INTRO ---
if st.session_state.current_page == "intro":
    
    st.markdown("""
    <div class='hero-container'>
        <h1 class='hero-title'>JACSICE Assistant.</h1>
        <p class='hero-subtitle'>Experience the next generation of campus navigation. A semantic neural network trained exclusively on Jayaraj Annapackiam CSI College data.</p>
    </div>
    
    <div class='feature-grid'>
        <div class='glass-card'>
            <div class='card-icon'>⚡</div>
            <div class='card-title'>Real-Time Data</div>
            <div class='card-text'>Instant semantic retrieval of courses, faculty, and placement statistics.</div>
        </div>
        <div class='glass-card'>
            <div class='card-icon'>👁️</div>
            <div class='card-title'>Visual Context</div>
            <div class='card-text'>Integrated multimedia rendering for campus locations and personnel.</div>
        </div>
        <div class='glass-card'>
            <div class='card-icon'>🗣️</div>
            <div class='card-title'>Natural Language</div>
            <div class='card-text'>Ask questions like you're talking to a human to instantly retrieve campus info.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") 
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Chat", use_container_width=True):
            st.session_state.current_page = "chat"
            st.rerun()

# --- PAGE 2: CHATBOT ---
elif st.session_state.current_page == "chat":

    if st.button("⬅️ Back to Home"):
        st.session_state.current_page = "intro"
        st.rerun()
        
    st.title("🏛️ JACSICE Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "Welcome to JACSICE! Ask me about our campus, placements, or faculty, and I might even show you some pictures!"}]
    
    if "is_busy" not in st.session_state:
        st.session_state.is_busy = False

    def lock_chat():
        st.session_state.is_busy = True

    for msg in st.session_state.chat_history:
        avatar = "🎓" if msg["role"] == "assistant" else "🧑‍💻"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    user_query = st.chat_input(
        "E.g., Can you show me the cricket ground?", 
        disabled=st.session_state.is_busy, 
        on_submit=lock_chat
    )

    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_query)

        groq_messages = [{"role": "system", "content": system_instruction}]
        for msg in st.session_state.chat_history:
            groq_messages.append({"role": msg["role"], "content": msg["content"]})

        with st.chat_message("assistant", avatar="🎓"):
            with st.spinner("Thinking... ✨"):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=groq_messages,
                        model="llama-3.1-8b-instant",
                        temperature=0.3
                    )
                    
                    response_text = chat_completion.choices[0].message.content
                    st.markdown(response_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                    
                    st.session_state.is_busy = False
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"API Error: {e}")
                    st.session_state.is_busy = False
                    st.stop()