import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Your CV information
cv_info = """
Name: Dominik Justin Späth
Education: 
- Studium Wirtschaftsinformatik, Euro FH, 03.2022 - present
- Ausbildung zur Fachkraft für Lagerlogistik, Simona AG, Kirn, 08.2014 - 06.2017
Experience:
- Projektleitung Machine Learning at Polytec-Group, Weierbach, 08.2023 - present
- Logistics Planning Specialist at Polytec-Group, Weierbach, 04.2024 - present
- Packaging Planner at Polytec-Group, Weierbach, 04.2023 - 03.2024
- Projektleitung at Manpaz Limited, Santiago de Chile, 08.2022 - 31.01.2023
- Lagerkoordinator at Simona AG, Kirn, 06.2017 - 07.2022
Skills: Project Management, Data Science, Machine Learning, Logistics, Supply Chain Management
Languages: German (native), English (fluent), Spanish (basic), Portuguese (basic)
"""

def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an AI assistant that answers questions about Dominik Späth based on his CV. Here is the CV information: {cv_info}"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI
st.title("Dominik Späth's Interactive CV")

# Display profile picture
profile_pic = st.sidebar.file_uploader("Upload a profile picture", type=["jpg", "png", "jpeg"])
if profile_pic is not None:
    st.sidebar.image(profile_pic, caption="Dominik Späth", use_column_width=True)
else:
    st.sidebar.write("No profile picture uploaded yet.")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Chat about CV", "Project Management App", "Data Science App", "Logistics App"])

with tab1:
    st.header("Chat about Dominik's Experience")
    st.write("Ask questions to learn more about Dominik's professional experience!")

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

with tab2:
    st.header("Project Management Application")
    st.write("This application showcases Dominik's project management skills.")
    st.info("Application under development. Check back soon for interactive project management tools!")
    if st.button("Visit Project Management App"):
        st.write("Redirecting to Project Management App...")
        # In a real scenario, you would use st.markdown to create a hyperlink
        # st.markdown("[Go to Project Management App](https://your-project-management-app-url)")

with tab3:
    st.header("Data Science Application")
    st.write("This application demonstrates Dominik's data science and machine learning capabilities.")
    st.info("Application under development. Check back soon for data analysis and ML demos!")
    if st.button("Visit Data Science App"):
        st.write("Redirecting to Data Science App...")
        # st.markdown("[Go to Data Science App](https://your-data-science-app-url)")

with tab4:
    st.header("Logistics Application")
    st.write("This application showcases Dominik's expertise in logistics and supply chain management.")
    st.info("Application under development. Check back soon for supply chain optimization tools!")
    if st.button("Visit Logistics App"):
        st.write("Redirecting to Logistics App...")
        # st.markdown("[Go to Logistics App](https://your-logistics-app-url)")

# Add information about the app
st.sidebar.title("About")
st.sidebar.info(
    "This app provides an interactive experience to learn about Dominik Späth's professional skills and experience. "
    "You can chat about Dominik's CV and explore specialized applications showcasing his expertise in "
    "project management, data science, and logistics."
)
st.sidebar.warning(
    "Note: This is a demo application. For the most accurate and current information about Dominik's experience, please contact him directly."
)