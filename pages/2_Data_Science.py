import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(page_title="Data Science Skills", page_icon="🧮")
st.title("Data Science and Machine Learning Skills")

# Sample dataset
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})

# Scatter plot
st.subheader("Sample Scatter Plot")
fig = px.scatter(df, x='x', y='y', color='category')
st.plotly_chart(fig)

# Simple ML model
st.subheader("Simple ML Model: Linear Regression")

X = df[['x']]
y = df['y']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

st.write(f"R-squared Score: {r2_score(y_test, y_pred):.2f}")
st.write(f"Mean Squared Error: {mean_squared_error(y_test, y_pred):.2f}")