import streamlit as st
import sys
import os

# Use pysqlite3 if it's available, otherwise fallback to sqlite3
try:
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
except ImportError:
    pass

from langchain_huggingface import HuggingFaceEndpoint
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# Set up Hugging Face API token
huggingface_token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
os.environ["HUGGINGFACEHUB_API_TOKEN"] = huggingface_token

# Initialize the language model
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",
    temperature=0.7,
    model_kwargs={"max_length": 512}
)

# Initialize the search tool
search = DuckDuckGoSearchAPIWrapper()

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

# Set up the conversation memory
memory = ConversationBufferMemory(return_messages=True)

# Set up the conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Streamlit UI
st.title("Dominik Späth's Interactive CV")

# Display profile picture
profile_pic = st.sidebar.file_uploader("Upload a profile picture", type=["jpg", "png", "jpeg"])
if profile_pic is not None:
    st.sidebar.image(profile_pic, caption="Dominik Späth", use_column_width=True)
else:
    st.sidebar.write("No profile picture uploaded yet.")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Chat with AI", "Project Management App", "Data Science App", "Logistics App"])

with tab1:
    st.header("Chat with AI about Dominik's Experience")
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
            full_response = conversation.predict(input=f"Based on this CV: {cv_info}\n\nUser question: {prompt}")
            st.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

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
    "You can chat with an AI assistant about Dominik's CV and explore specialized applications showcasing his expertise in "
    "project management, data science, and logistics."
)
st.sidebar.warning(
    "Note: While the AI assistant can answer questions based on the provided CV, "
    "for the most accurate and current information about Dominik's experience, please contact him directly."
)