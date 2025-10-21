import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Your updated CV information
cv_info = """
Name: Dominik Justin Späth
Birthday: March 30, 1998
Email: dominik_justin@outlook.de

Education:
- Studium Wirtschaftsinformatik, Euro FH, 03.2022 - present
- Ausbildung zur Fachkraft für Lagerlogistik, Simona AG, Kirn, 08.2014 - 06.2017
- Realschule plus, Kirn, 08.2008 - 07.2014 (Mittlere Reife)

Experience:
- Projektleitung Machine Learning at Polytec-Group, Weierbach, 08.2023 - present
  • Leading machine learning projects with full budget responsibility
  • Implementing ML technologies in the painting process, significantly improving the "First Run Rate"
  • Coordinating between project teams and external service providers
  • Creating project reports for board and management
  • Developing and determining internal KPIs
  • Process development and optimization in the context of ML integration

- Logistics Planning Specialist at Polytec-Group, Weierbach, 04.2023 - present
  • Developing and optimizing end-to-end logistics concepts
  • Leading interdisciplinary teams and managing resource allocation in projects
  • Developing global standard processes and implementing local process variations
  • Ensuring structured documentation and quality management
  • Proactive risk identification and management

- Projektleitung at Manpaz Limited, Santiago de Chile, 08.2022 - 31.01.2023
  • Acquiring new orders and building customer relationships
  • Developing and optimizing production processes
  • Leading outsourcing projects to China, leveraging free trade agreements
  • Managing project budgets and optimizing resource utilization

- Fachkraft für Lagerlogistik at Simona AG, Kirn, 06.2017 - 07.2022
  • Versatile role in all warehouse areas, focusing on goods receipt, dispatch, and storage
  • Operating technical commissioning systems
  • Contributing to quality control, inventory management, and stocktaking
  • Active involvement in improving the WACOS warehouse management software
  • Implementing new packaging standards and optimizing commissioning processes
  • Serving as a safety officer, achieving over 1000 consecutive accident-free days

Skills:
- Project Management: Budget responsibility, team leadership, risk management, KPI development
- Machine Learning: Implementation in industrial processes, particularly in painting processes
- Logistics: End-to-end logistics concept development, process optimization, supply chain management
- Data Analysis: Developing and determining KPIs, creating project reports
- Quality Management: Structured documentation, continuous improvement processes
- Safety Management: Experience as a safety officer in industrial settings

Technical Skills:
- ERP Systems: SAP R3/SAP 4 Hana
- CAD Software: Creo CAD, Solidworks CAD
- Data Analysis: MS Power BI/Power Apps
- Project Management Tools: MS-Project, MS-Azure, Asana, Jira
- Programming: Python
- Warehouse Management: WACOS, Ipolog
- AI Frameworks: CrewAI

Languages:
- German: Native
- English: Fluent
- Spanish: Basic knowledge
- Portuguese: Basic knowledge

Soft Skills:
- Strong analytical and problem-solving abilities
- Excellent communication and presentation skills
- Team leadership and motivation
- Adaptability and quick learning in new environments
- Attention to detail and quality-focused

Personality Traits:
- Proactive and self-motivated
- Hands-on mentality and technical understanding
- Intercultural competence
- Collaborative team player with a positive attitude
- Thrives in fast-paced, challenging environments

Career Goals:
- To drive innovation in logistics and production processes through machine learning and AI
- To contribute to sustainable and efficient industrial practices
- To continue developing expertise in project management and team leadership

Personal:
- Married
"""

def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        st.warning(f"Profile image not found: {image_path}")
        return None

def send_email(name, email, message):
    sender_email = "dominikjustinspath@gmail.com"
    sender_password = st.secrets["GMAIL_APP_PASSWORD"]
    receiver_email = "dominik_justin@outlook.de"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"New contact from {name} via Interactive CV"

    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def get_interactive_cv_response(prompt, conversation_history):
    try:
        messages = [
            {"role": "system", "content": f"""You are an AI assistant representing Dominik Späth, capable of discussing his CV and showcasing his skills. 
            You have access to Dominik's CV and should answer questions based on this information: {cv_info}
            
            When responding:
            - Be professional yet approachable
            - Show enthusiasm for technology, especially AI and machine learning
            - Demonstrate a strong analytical mindset
            - Express a collaborative and positive attitude
            - Highlight Dominik's problem-solving skills and adaptability
            - When appropriate, mention his interest in sustainability and industry trends
            
            If asked about specific skills or challenges:
            1. Interpret the task in the context of Dominik's skills
            2. Provide a detailed explanation of how Dominik's skills apply to the task
            3. If relevant, suggest a hypothetical code snippet or data analysis approach
            4. Relate the solution to industry trends or best practices
            
            Provide informative answers, and be ready to elaborate on specific skills or experiences.
            
            Remember to mention that Dominik is married if asked about his personal life."""}
        ]
        
        # Add conversation history to messages
        messages.extend(conversation_history)
        
        # Add the new user prompt
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Dominik Späth's Interactive CV", page_icon="📄", layout="wide")

# Custom CSS for modern design
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Root variables for consistent theming */
    :root {
        --primary-color: #2563eb;
        --primary-dark: #1e40af;
        --primary-light: #3b82f6;
        --secondary-color: #10b981;
        --accent-color: #8b5cf6;
        --background-primary: #ffffff;
        --background-secondary: #f8fafc;
        --background-tertiary: #f1f5f9;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-light: #94a3b8;
        --border-color: #e2e8f0;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }

    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }

    .main {
        background-color: transparent;
        padding: 2rem 1rem;
    }

    /* Modern container with glassmorphism */
    .block-container {
        max-width: 1200px;
        padding: 2rem 3rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        box-shadow: var(--shadow-xl);
        animation: fadeIn 0.5s ease-in;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Title styling */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 3rem !important;
        margin-bottom: 2rem !important;
        letter-spacing: -0.02em;
    }

    h2 {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1.875rem !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.01em;
    }

    /* Tabs styling */
    .stTabs {
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--background-tertiary);
        padding: 6px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
        padding: 0 24px;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.5);
        color: var(--primary-color);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: var(--shadow-md);
    }

    /* Chat message styling */
    .stChatMessage {
        background-color: var(--background-secondary);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
        animation: slideIn 0.4s ease;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .stChatMessage:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }

    /* User message - different styling */
    .stChatMessage[data-testid*="user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    .stChatMessage[data-testid*="user"] p {
        color: white !important;
    }

    /* Assistant message */
    .stChatMessage[data-testid*="assistant"] {
        background-color: white;
        border: 1px solid var(--border-color);
    }

    /* Chat input styling */
    .stChatInputContainer {
        border-top: 1px solid var(--border-color);
        padding-top: 1rem;
        margin-top: 2rem;
    }

    .stChatInput {
        border-radius: 12px !important;
        border: 2px solid var(--border-color) !important;
        transition: all 0.3s ease !important;
    }

    .stChatInput:focus-within {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 252, 0.98) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid var(--border-color);
        padding: 2rem 1rem;
    }

    [data-testid="stSidebar"] .sidebar-img {
        border: 4px solid white;
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
    }

    [data-testid="stSidebar"] .sidebar-img:hover {
        transform: scale(1.05);
        box-shadow: var(--shadow-xl);
    }

    [data-testid="stSidebar"] h1 {
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: var(--shadow-sm);
        animation: fadeIn 0.5s ease;
    }

    /* Form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid var(--border-color);
        padding: 12px 16px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Success/Error messages */
    .stSuccess {
        background-color: #d1fae5;
        color: #065f46;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid var(--secondary-color);
    }

    .stError {
        background-color: #fee2e2;
        color: #991b1b;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #ef4444;
    }

    .stWarning {
        background-color: #fef3c7;
        color: #92400e;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #f59e0b;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--background-tertiary);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }

    /* Loading animation */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .block-container {
            padding: 1.5rem 1rem;
            border-radius: 16px;
        }

        h1 {
            font-size: 2rem !important;
        }

        h2 {
            font-size: 1.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("Dominik Späth's Interactive CV")

# Create tabs for different sections
tab1, tab2 = st.tabs(["💬 Interaktiver CV Chat", "📧 Kontakt"])

with tab1:
    st.header("💬 Chat mit Dominiks KI-Assistent")

    # Chat container
    chat_container = st.container()

    with chat_container:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 4px solid #667eea;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        ">
            <h3 style="color: #1e293b; margin-top: 0; font-size: 1.3rem;">👋 Willkommen!</h3>
            <p style="color: #475569; line-height: 1.8; margin-bottom: 0;">
                Ich bin ein KI-Assistent, der Dominik Späth repräsentiert. Ich kann dir Informationen über seine
                berufliche Erfahrung, Fähigkeiten und Interessen geben – mit Schwerpunkt auf seine aktuellen Rollen
                im <strong>Machine Learning Projektmanagement</strong> und der <strong>Logistikplanung</strong>.<br><br>

                Du kannst mich gerne über seine Karriere befragen, Herausforderungen vorschlagen oder nach
                spezifischen Fähigkeiten in Bereichen wie Machine Learning, Logistikoptimierung oder
                Projektmanagement fragen.<br><br>

                <strong>Was möchtest du wissen?</strong> 🚀
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Input container
    input_container = st.container()
    
    with input_container:
        # React to user input
        if prompt := st.chat_input("Was möchtest du wissen oder besprechen?"):
            # Display user message in chat message container
            with chat_container:
                st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            with chat_container:
                with st.chat_message("assistant"):
                    response = get_interactive_cv_response(prompt, st.session_state.messages)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Sidebar content with enhanced styling
    profile_pic_base64 = get_image_base64("dominik_profile.jpg")
    if profile_pic_base64:
        st.sidebar.markdown(
            f"""
            <style>
            .sidebar-img {{
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 150px;
                border-radius: 50%;
            }}
            .profile-name {{
                text-align: center;
                font-size: 1.5rem;
                font-weight: 700;
                color: #1e293b;
                margin: 1.5rem 0 0.5rem 0;
            }}
            .profile-info {{
                text-align: center;
                color: #64748b;
                font-size: 0.95rem;
                margin: 0.5rem 0;
                line-height: 1.6;
            }}
            .profile-email {{
                text-align: center;
                color: #667eea;
                font-size: 0.9rem;
                margin: 1rem 0;
                word-break: break-all;
            }}
            .profile-divider {{
                height: 2px;
                background: linear-gradient(90deg, transparent, #667eea, transparent);
                margin: 1.5rem 0;
            }}
            </style>
            <img src="data:image/jpeg;base64,{profile_pic_base64}" class="sidebar-img">
            <div class="profile-name">Dominik Späth</div>
            <div class="profile-divider"></div>
            <div class="profile-info">📅 Geboren: 30. März 1998</div>
            <div class="profile-email">✉️ dominik_justin@outlook.de</div>
            """,
            unsafe_allow_html=True
        )

with tab2:
    st.header("📧 Kontaktiere Dominik")

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 4px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    ">
        <p style="color: #475569; line-height: 1.8; margin-bottom: 0;">
            Nutze dieses Formular, um eine Nachricht direkt an Dominik zu senden.
            Ich werde mich so schnell wie möglich bei dir melden! 📬
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("contact_form"):
        name = st.text_input("📝 Dein Name", placeholder="Max Mustermann")
        email = st.text_input("✉️ Deine E-Mail", placeholder="max.mustermann@beispiel.de")
        message = st.text_area("💬 Deine Nachricht", placeholder="Hallo Dominik, ich würde gerne mit dir über...", height=150)
        submit_button = st.form_submit_button("📤 Nachricht senden")

    if submit_button:
        if name and email and message:
            if send_email(name, email, message):
                st.success("✅ Deine Nachricht wurde erfolgreich versendet!")
            else:
                st.error("❌ Beim Versenden der Nachricht ist ein Fehler aufgetreten. Bitte versuche es später erneut.")
        else:
            st.warning("⚠️ Bitte fülle alle Felder aus, bevor du die Nachricht sendest.")

# Add information about the app
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="margin-top: 2rem;">
    <h3 style="color: #1e293b; font-size: 1.2rem; margin-bottom: 1rem;">ℹ️ Über diese App</h3>
    <p style="color: #64748b; font-size: 0.9rem; line-height: 1.6;">
        Diese App bietet ein interaktives Erlebnis, um mehr über Dominik Späths
        berufliche Fähigkeiten und Erfahrungen zu erfahren. Du kannst über seinen
        Lebenslauf chatten, seine Skills erkunden und über das Kontaktformular
        in Verbindung treten.
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="
    background-color: #fef3c7;
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1.5rem;
">
    <p style="color: #92400e; font-size: 0.85rem; line-height: 1.5; margin: 0;">
        <strong>Hinweis:</strong> Dies ist eine Demo-Anwendung. Für die aktuellsten
        Informationen kontaktiere Dominik bitte direkt.
    </p>
</div>
""", unsafe_allow_html=True)