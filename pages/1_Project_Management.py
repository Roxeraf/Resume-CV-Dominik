import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Project Management Skills", page_icon="📊")
st.title("Project Management Skills")

# Gantt Chart
st.subheader("Sample Gantt Chart")
df = pd.DataFrame([
    dict(Task="Research", Start='2024-01-01', Finish='2024-02-15', Department="Planning"),
    dict(Task="Design", Start='2024-02-16', Finish='2024-03-31', Department="Development"),
    dict(Task="Development", Start='2024-04-01', Finish='2024-07-31', Department="Development"),
    dict(Task="Testing", Start='2024-08-01', Finish='2024-09-15', Department="QA"),
    dict(Task="Deployment", Start='2024-09-16', Finish='2024-10-15', Department="Operations")
])
fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Department")
st.plotly_chart(fig)

# Risk Matrix
st.subheader("Sample Risk Matrix")
risks = pd.DataFrame({
    'Risk': ['Technical Failure', 'Budget Overrun', 'Scope Creep', 'Resource Unavailability'],
    'Probability': [0.2, 0.4, 0.6, 0.3],
    'Impact': [0.8, 0.6, 0.5, 0.7]
})
fig = px.scatter(risks, x='Probability', y='Impact', text='Risk', 
                 title='Risk Matrix', labels={'Probability': 'Probability', 'Impact': 'Impact'})
fig.update_traces(textposition='top center')
fig.update_layout(xaxis_range=[0,1], yaxis_range=[0,1])
st.plotly_chart(fig)