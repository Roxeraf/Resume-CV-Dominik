import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Your CV information
cv_info = """
Name: Dominik Justin Späth
Birthday: March 30, 1998
Email: dominik_justin@outlook.de

Education: 
- Studium Wirtschaftsinformatik, Euro FH, 03.2022 - present
- Ausbildung zur Fachkraft für Lagerlogistik, Simona AG, Kirn, 08.2014 - 06.2017

Experience:
- Projektleitung Machine Learning at Polytec-Group, Weierbach, 08.2023 - present
  • Leading machine learning projects in the automotive industry
  • Implementing AI solutions for quality control and process optimization
- Logistics Planning Specialist at Polytec-Group, Weierbach, 04.2024 - present
  • Optimizing supply chain processes using data-driven approaches
  • Developing and implementing logistics strategies
- Packaging Planner at Polytec-Group, Weierbach, 04.2023 - 03.2024
  • Designing efficient packaging solutions for automotive components
  • Reducing packaging costs while improving product protection
- Projektleitung at Manpaz Limited, Santiago de Chile, 08.2022 - 31.01.2023
  • Led international projects in a Spanish-speaking environment
  • Gained valuable experience in cross-cultural communication
- Lagerkoordinator at Simona AG, Kirn, 06.2017 - 07.2022
  • Managed warehouse operations and inventory control
  • Implemented lean management principles to improve efficiency

Skills:
- Project Management: Agile methodologies, Scrum, Kanban, risk management, stakeholder communication
- Data Science: Python, SQL, data visualization (Tableau, Power BI), statistical analysis
- Machine Learning: TensorFlow, PyTorch, scikit-learn, deep learning, computer vision
- Logistics: Supply chain optimization, inventory management, warehouse management systems (WMS)
- Supply Chain Management: Demand forecasting, route optimization, logistics network design
- Languages: German (native), English (fluent), Spanish (conversational), Portuguese (basic)

Technical Skills:
- Programming: Python, SQL, Java (basic)
- Tools: Git, Docker, Kubernetes, AWS, Azure
- Databases: MySQL, PostgreSQL, MongoDB
- BI Tools: Tableau, Power BI, QlikView
- AI/ML: Agentic frameworks, prompt engineering, training LLM models
- ERP Systems: SAP
- Data Science: Python, SQL, data visualization (Tableau, Power BI), statistical analysis

Soft Skills:
- Strong analytical and problem-solving abilities
- Excellent communication and presentation skills
- Team leadership and motivation
- Adaptability and quick learning in new environments
- Attention to detail and quality-focused

Personality Traits:
- Proactive and self-motivated
- Curious and always eager to learn new technologies
- Collaborative team player with a positive attitude
- Thrives in fast-paced, challenging environments
- Values work-life balance and practices mindfulness

Interests:
- Staying up-to-date with the latest trends in AI and machine learning
- Contributing to open-source projects in logistics and supply chain optimization
- Mentoring junior data scientists and logistics professionals
- Exploring the intersection of sustainability and supply chain management

Career Goals:
- To become a thought leader in the application of AI in logistics and supply chain management
- To drive digital transformation in the automotive industry through innovative AI solutions
- To contribute to the development of more sustainable and efficient logistics practices
"""

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

def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        st.warning(f"Profile image not found: {image_path}")
        return None

def get_openai_response(prompt):
    try:
        if "contact" in prompt.lower() or "get in touch" in prompt.lower():
            return "If you'd like to get in touch with Dominik, please use the contact form below. You can leave your message and contact information there, and Dominik will get back to you soon."
        elif "weakness" in prompt.lower() or "weaknesses" in prompt.lower():
            weakness_response = """One of my main areas for improvement is my tendency to become deeply engrossed in projects, sometimes to the point where I may lose track of time or overlook other tasks. This stems from my passion for problem-solving and my drive to see projects through to completion.

While this intense focus allows me to produce high-quality work and innovative solutions, I've recognized the need to balance this with better time management and a broader perspective on project priorities. To address this, I've been:

1. Implementing stricter time-boxing techniques to allocate specific periods for different tasks.
2. Regularly stepping back to reassess project priorities and ensure I'm aligning with overall team and organizational goals.
3. Actively seeking feedback from colleagues and supervisors to maintain a well-rounded view of my work and its impact.

This self-awareness and the steps I'm taking to improve have actually enhanced my project management skills and my ability to collaborate effectively with teams. It's an ongoing process, but I've already seen positive results in terms of increased productivity and more balanced project outcomes."""

            return weakness_response
        else:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using the specified model
                messages=[
                    {"role": "system", "content": f"""You are an AI assistant representing Dominik Späth. 
                    You have access to Dominik's CV and should answer questions based on this information: {cv_info}
                    
                    When responding, embody Dominik's personality:
                    - Be professional yet approachable
                    - Show enthusiasm for technology, especially AI and machine learning
                    - Demonstrate a strong analytical mindset
                    - Express a collaborative and positive attitude
                    - Highlight your problem-solving skills and adaptability
                    - When appropriate, mention your interest in sustainability and industry trends
                    
                    Provide concise but informative answers, and be ready to elaborate on specific skills or experiences if asked."""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main app
st.set_page_config(page_title="Dominik Späth's Interactive CV", page_icon="📄", layout="wide")
st.title("Dominik Späth's Interactive CV")

# Sidebar
profile_pic_base64 = get_image_base64("dominik_profile.jpg")
if profile_pic_base64:
    st.sidebar.image(f"data:image/jpeg;base64,{profile_pic_base64}", width=150)

st.sidebar.write("Dominik Späth")
st.sidebar.write("Born: March 30, 1998")
st.sidebar.write("Email: dominik_justin@outlook.de")

st.sidebar.title("About")
st.sidebar.info(
    "This app provides an interactive experience to learn about Dominik Späth's professional skills and experience. "
    "You can chat about Dominik's CV and get in touch using the contact form below."
)
st.sidebar.warning(
    "Note: This is a demo application. For the most accurate and current information about Dominik's experience, please contact him directly."
)

# Main content
st.header("Chat with Dominik's AI Assistant")
st.write("""
Hello! I'm an AI assistant representing Dominik Späth. I can tell you about Dominik's professional experience, 
skills, and interests. Feel free to ask me anything about his career in project management, data science, 
machine learning, or logistics. What would you like to know?
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to know?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = get_openai_response(prompt)
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Contact Form
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