"""
Robi.AI - Interactive Portfolio Assistant for Robin Jimmichan P
Optimized version with external context file
"""

import streamlit as st
from groq import Groq
from context import ROBIN_CONTEXT, SAMPLE_QUESTIONS

# Page configuration
st.set_page_config(
    page_title="Ask Robi.AI",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for branding
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
    }
    .main-header p {
        color: #f0f0f0;
        margin: 0.5rem 0 0 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🤖 Ask Robi.AI</h1>
        <p>Your Interactive Guide to Robin's Business Analytics Portfolio</p>
    </div>
    """, unsafe_allow_html=True)

st.write("👋 Hi! I'm Robin's AI assistant. Ask me anything about his 21 projects, skills, or approach to Business Analytics!")

# Initialize Groq client
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Please add your GROQ_API_KEY to Streamlit secrets to enable the chatbot.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hi there! I'm here to help you explore Robin's Business Analytics portfolio with **21 real-world projects**. You can ask me about:\n\n" +
                   "📊 **Excel Projects** (6 projects): Bank Segmentation, E-commerce, HR Analytics, Marketing ROI, Sales, Telco Churn\n" +
                   "🗃️ **SQL Projects** (6 projects): Inventory, Loan Risk, Hospital Records, Bank Segmentation, Telco Churn, Healthcare Claims\n" +
                   "📈 **Power BI Projects** (5 projects): Retail Sales, Financial P&L, Customer 360, E-commerce Funnel, Telco Churn\n" +
                   "🐍 **Python Projects** (4 projects): Sales Forecasting (92% accuracy), Basket Analysis, Airbnb, Healthcare\n" +
                   "💼 His approach to solving business problems\n" +
                   "🎯 Specific technical skills or measurable business impact\n" +
                   "📊 Project methodologies and how achievements were reached\n\n" +
                   "What would you like to know?"
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about Robin's projects, skills, or approach..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": ROBIN_CONTEXT},
                        *[{"role": m["role"], "content": m["content"]} 
                          for m in st.session_state.messages[1:]]  # Skip welcome message
                    ],
                    temperature=0.7,
                    max_tokens=1200,
                    top_p=0.9
                )
                
                assistant_response = response.choices[0].message.content
                st.markdown(assistant_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Sidebar with info
with st.sidebar:
    st.markdown("### 🎯 About This Assistant")
    st.write("This AI chatbot helps visitors understand Robin's Business Analytics portfolio with **21 real projects across 10 industries**.")
    
    st.markdown("### 📚 Quick Links")
    st.markdown("- [GitHub Profile](https://github.com/Robi8995)")
    st.markdown("- [LinkedIn](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)")
    st.markdown("- [Excel Projects Repo](https://github.com/Robi8995/Business-Analyst-Excel-Projects)")
    st.markdown("- [SQL Projects Repo](https://github.com/Robi8995/Business-Analyst-SQL-Projects)")
    st.markdown("- [Python Projects Repo](https://github.com/Robi8995/Business-Analyst-Python-Projects)")
    st.markdown("- [Power BI Projects Repo](https://github.com/Robi8995/Business-Analyst-Power-BI-Projects)")
    
    st.markdown("### 💡 Sample Questions")
    st.info("\n".join([f"- {q}" for q in SAMPLE_QUESTIONS[:8]]))
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Portfolio Stats")
    st.metric("Total Projects", "21")
    st.metric("Excel Projects", "6")
    st.metric("SQL Projects", "6")
    st.metric("Power BI Projects", "5")
    st.metric("Python Projects", "4")
    st.metric("Industries Covered", "10")
    
    st.markdown("---")
    st.markdown("### 🎖️ Key Achievements")
    st.success("✅ 92% Forecasting Accuracy")
    st.success("✅ 15-20% Cost Reduction")
    st.success("✅ 60% VIP Revenue ID")
    st.success("✅ 28% High-Risk Detection")
    
    st.markdown("---")
    st.caption("Built with ❤️ by Robin | Powered by Groq (Llama 3.3)")

