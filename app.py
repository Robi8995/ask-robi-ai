import streamlit as st
from groq import Groq
import os

# --------------------------- #
# PAGE CONFIGURATION
# --------------------------- #
st.set_page_config(
    page_title="Ask Robi.AI",
    page_icon="🤖",
    layout="centered"
)

# --------------------------- #
# STYLES
# --------------------------- #
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 { color: white; margin: 0; }
    .main-header p { color: #f0f0f0; margin: 0.5rem 0 0 0; }
    </style>
""", unsafe_allow_html=True)

# --------------------------- #
# HEADER
# --------------------------- #
st.markdown("""
<div class="main-header">
    <h1>🤖 Ask Robi.AI</h1>
    <p>Your Interactive Guide to Robin's Business Analytics Portfolio</p>
</div>
""", unsafe_allow_html=True)

st.write("👋 Hi! I'm Robin's AI assistant. Ask me anything about his 21 projects, skills, or approach to Business Analytics!")

# --------------------------- #
# API KEY CHECK
# --------------------------- #
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Please add your GROQ_API_KEY to Streamlit secrets to enable the chatbot.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --------------------------- #
# LOAD CONTEXT (cached)
# --------------------------- #
@st.cache_data
def load_context():
    path = "context.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "Context file not found. Please upload `context.txt` with all project details."

context = load_context()

# --------------------------- #
# CHAT INITIALIZATION
# --------------------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "👋 Hi there! I'm here to help you explore Robin's **21 Business Analytics projects**.\n\n"
            "You can ask about:\n"
            "- 📊 Excel Projects (6)\n"
            "- 🗃️ SQL Projects (5)\n"
            "- 📈 Power BI Projects (4)\n"
            "- 🐍 Python Projects (4)\n"
            "- 🎯 Achievements, KPIs, and methods\n"
            "What would you like to know?"
        )
    })

# --------------------------- #
# DISPLAY CHAT HISTORY
# --------------------------- #
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------- #
# CHAT INPUT
# --------------------------- #
prompt = st.chat_input("Ask about Robin's projects, skills, or approach...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": (
                            "You are Robi.AI — a portfolio chatbot for Robin Jimmichan P, "
                            "a Business Analyst with 21 projects. "
                            "Answer with enthusiasm, business focus, and precise technical detail. "
                            "Reference specific metrics and tools from context below.\n\n"
                            f"=== CONTEXT ===\n{context[:15000]}"  # limits to 15k chars to stay efficient
                        )},
                        *[{"role": m["role"], "content": m["content"]}
                          for m in st.session_state.messages[-8:]]  # use only recent history
                    ],
                    temperature=0.7,
                    max_tokens=800
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

            except Exception as e:
                st.error(f"❌ Error: {e}")

# --------------------------- #
# SIDEBAR
# --------------------------- #
with st.sidebar:
    st.markdown("### 🎯 About This Assistant")
    st.write("AI chatbot that explains Robin's **21 real-world analytics projects**.")

    st.markdown("### 📚 Quick Links")
    st.markdown("""
    - [GitHub](https://github.com/Robi8995)
    - [LinkedIn](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)
    - [Excel Projects](https://github.com/Robi8995/Business-Analyst-Excel-Projects)
    - [SQL Projects](https://github.com/Robi8995/Business-Analyst-SQL-Projects)
    - [Python Projects](https://github.com/Robi8995/Business-Analyst-Python-Projects)
    - [Power BI Projects](https://github.com/Robi8995/Business-Analyst-Power-BI-Projects)
    """)

    st.markdown("### 💡 Sample Questions")
    st.info("""
    Try asking:
    - "How did Robin achieve 92% forecasting accuracy?"
    - "Explain the E-commerce Funnel Dashboard"
    - "Which project shows 15-20% cost reduction?"
    - "How was 28% high-risk detection achieved?"
    """)

    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.metric("Total Projects", "21")
    st.metric("Industries", "10")
    st.metric("Forecast Accuracy", "92%")
    st.metric("Cost Reduction", "20%")
    st.metric("VIP Revenue Share", "60%")
    st.metric("Churn Detection Gain", "15%")

    st.markdown("---")
    st.caption("Built by Robin • Powered by Groq + Streamlit")
