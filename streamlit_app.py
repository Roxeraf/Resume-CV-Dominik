import streamlit as st
import sys
import os

# Use pysqlite3 if it's available, otherwise fallback to sqlite3
try:
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
except ImportError:
    pass

from crewai import Agent, Task, Crew
from langchain_huggingface import HuggingFaceEndpoint
from langchain.tools import Tool
from langchain.utilities import DuckDuckGoSearchAPIWrapper
import pandas as pd
import matplotlib.pyplot as plt
import io
import networkx as nx
import seaborn as sns
from sklearn.cluster import KMeans
import numpy as np

# Set up Hugging Face API token
huggingface_token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
os.environ["HUGGINGFACEHUB_API_TOKEN"] = huggingface_token

# Initialize the language model
llm = HuggingFaceEndpoint(repo_id="google/flan-t5-large", model_kwargs={"temperature": 0.5, "max_length": 512})

# Initialize the search tool
search = DuckDuckGoSearchAPIWrapper()
search_tool = Tool(
    name="Search",
    func=search.run,
    description="useful for when you need to answer questions about current events"
)

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

# Custom tools
def create_gantt_chart(project_tasks):
    """Create a Gantt chart for project tasks."""
    tasks = eval(project_tasks)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(range(len(tasks)), [task['duration'] for task in tasks], left=[task['start'] for task in tasks])
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([task['task'] for task in tasks])
    ax.set_xlabel('Timeline')
    ax.set_title('Project Gantt Chart')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    st.image(buf)
    return "Gantt chart created and displayed."

def perform_data_analysis(data_description):
    """Perform a simple data analysis and visualization."""
    data = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D'],
        'Value': [4, 7, 2, 9]
    })
    fig, ax = plt.subplots()
    data.plot(kind='bar', x='Category', y='Value', ax=ax)
    ax.set_title('Data Analysis Result')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    st.image(buf)
    return f"Data analysis performed on {data_description}. Bar chart created and displayed."

def optimize_route(locations):
    """Simulate route optimization for logistics."""
    optimized_route = ['Start'] + sorted(eval(locations)) + ['End']
    st.write(f"Optimized Route: {' -> '.join(optimized_route)}")
    return f"Route optimized for locations: {locations}"

def read_excel_file(file):
    """Read an Excel file and return its contents as a DataFrame."""
    try:
        df = pd.read_excel(file)
        return df.to_dict()
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Define tools
gantt_tool = Tool(
    name="Create Gantt Chart",
    func=create_gantt_chart,
    description="Create a Gantt chart for project tasks"
)

data_analysis_tool = Tool(
    name="Perform Data Analysis",
    func=perform_data_analysis,
    description="Perform a simple data analysis and visualization"
)

route_optimization_tool = Tool(
    name="Optimize Route",
    func=optimize_route,
    description="Simulate route optimization for logistics"
)

excel_tool = Tool(
    name="Read Excel File",
    func=read_excel_file,
    description="Read an Excel file and return its contents"
)

# Define agents
project_manager = Agent(
    role='Project Manager',
    goal='Manage projects and coordinate team efforts',
    backstory=f"An experienced project manager with a background in: {cv_info}",
    verbose=True,
    llm=llm,
    tools=[search_tool, gantt_tool, excel_tool]
)

data_scientist = Agent(
    role='Data Scientist',
    goal='Analyze data and implement machine learning solutions',
    backstory=f"A skilled data scientist with experience in: {cv_info}",
    verbose=True,
    llm=llm,
    tools=[search_tool, data_analysis_tool, excel_tool]
)

logistics_specialist = Agent(
    role='Logistics Specialist',
    goal='Optimize logistics processes and improve efficiency',
    backstory=f"An expert in logistics with a history of: {cv_info}",
    verbose=True,
    llm=llm,
    tools=[search_tool, route_optimization_tool, excel_tool]
)

# Streamlit UI
st.title("Interactive CV Experience with Dominik Späth")
st.write("Ask questions or propose scenarios to interact with different aspects of Dominik's professional experience!")

# File upload
uploaded_file = st.file_uploader("Upload an Excel file (optional)", type="xlsx")

# User input
user_input = st.text_input("Enter your question or scenario:")

if user_input:
    # Create tasks based on user input
    task1 = Task(
        description=f"Respond to the user's input from a project management perspective: {user_input}",
        agent=project_manager
    )

    task2 = Task(
        description=f"Analyze the user's input from a data science perspective: {user_input}",
        agent=data_scientist
    )

    task3 = Task(
        description=f"Consider the logistics implications of the user's input: {user_input}",
        agent=logistics_specialist
    )

    # Create and run the crew
    crew = Crew(
        agents=[project_manager, data_scientist, logistics_specialist],
        tasks=[task1, task2, task3],
        verbose=2
    )

    with st.spinner("Generating responses..."):
        result = crew.kickoff()

    # Display results
    st.subheader("Responses:")
    st.write(result)

# Test Hugging Face Model
if st.button("Test Hugging Face Model"):
    with st.spinner("Testing the model..."):
        try:
            response = llm("Translate the following English text to French: 'Hello, how are you?'")
            st.success(f"Model response: {response}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Add information about the app
st.sidebar.title("About")
st.sidebar.info(
    "This app showcases Dominik Späth's skills in project management, data science, and logistics. "
    "The AI agents can access the internet and use custom tools to demonstrate specific capabilities."
)
st.sidebar.warning(
    "Note: While the AI agents can search for current information and use custom tools, their core knowledge is based on the provided CV. "
    "For the most accurate and current information about Dominik's experience, please contact him directly."
)