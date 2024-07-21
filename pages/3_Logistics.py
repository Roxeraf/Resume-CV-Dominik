import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Logistics Skills", page_icon="🚚")
st.title("Logistics and Supply Chain Management Skills")

# Simple inventory management
st.subheader("Inventory Management")
inventory = pd.DataFrame({
    'Product': ['A', 'B', 'C', 'D'],
    'Quantity': [100, 150, 80, 120],
    'Reorder Point': [50, 75, 40, 60]
})
st.dataframe(inventory)

# Supply chain network
st.subheader("Supply Chain Network")
G = nx.Graph()
G.add_edges_from([('Supplier', 'Warehouse'), ('Warehouse', 'Distribution Center'), 
                  ('Distribution Center', 'Retailer 1'), ('Distribution Center', 'Retailer 2')])
pos = nx.spring_layout(G)
fig, ax = plt.subplots()
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold')
st.pyplot(fig)