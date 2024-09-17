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

# Custom CSS to create a static input field at the bottom
st.markdown("""
<style>
.stApp {
    margin: 0;
    padding: 0;
    overflow: hidden;
}
.main {
    display: flex;
    flex-direction: column;
    height: 100vh;
}
.chat-container {
    flex-grow: 1;
    overflow-y: auto;
    padding: 10px;
}
.input-container {
    position: sticky;
    bottom: 0;
    background-color: white;
    padding: 10px;
    border-top: 1px solid #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

st.title("Dominik Späth's Interactive CV")

# Create tabs for different sections
tab1, tab2 = st.tabs(["Interactive CV Chat", "Contact"])

with tab1:
    st.header("Chat with Dominik's AI Assistant")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        st.write("""
        Hello! I'm an AI assistant representing Dominik Späth. I can tell you about Dominik's professional experience, 
        skills, and interests, with a focus on his current roles in Machine Learning Project Management and Logistics Planning. 
        Feel free to ask me anything about his career, propose challenges, or inquire about 
        specific skills in areas like machine learning, logistics optimization, or project management. 
        What would you like to know?
        """)

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
        if prompt := st.chat_input("What would you like to know or discuss?"):
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

    # Sidebar content
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
            </style>
            <img src="data:image/jpeg;base64,{profile_pic_base64}" class="sidebar-img">
            """,
            unsafe_allow_html=True
        )
    st.sidebar.write("Dominik Späth")
    st.sidebar.write("Born: March 30, 1998")
    st.sidebar.write("Email: dominik_justin@outlook.de")

with tab2:
    st.header("Contact Dominik")
    st.write("Use this form to send a message directly to Dominik.")
    
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submit_button = st.form_submit_button("Send Message")

    if submit_button:
        if name and email and message:
            if send_email(name, email, message):
                st.success("Your message has been sent successfully!")
            else:
                st.error("There was an error sending your message. Please try again later.")
        else:
            st.warning("Please fill out all fields before sending.")

# Add information about the app
st.sidebar.title("About")
st.sidebar.info(
    "This app provides an interactive experience to learn about Dominik Späth's professional skills and experience. "
    "You can chat about Dominik's CV, explore his skills, and get in touch using the contact form."
)
st.sidebar.warning(
    "Note: This is a demo application. For the most accurate and current information about Dominik's experience, please contact him directly."
)