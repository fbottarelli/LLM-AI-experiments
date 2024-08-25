import streamlit as st
import sqlite3
import pandas as pd
import json
import plotly.express as px

# hard coded paths
path_data = 'data/data.json'
path_sqlite = 'data/sqlite/blood_analysis.db'

# Load selected features and customers from data.json
with open(path_data, 'r') as f:
    data = json.load(f)
    selected_features = data['test_names_selected']
    customers = data['customers']

# Connect to the SQLite database
conn = sqlite3.connect(path_sqlite)

# Streamlit app
st.title('Blood Analysis Dashboard')

# list of tables in the database
query = "SELECT name FROM sqlite_master WHERE type='table'"
tables = pd.read_sql_query(query, conn)['name'].tolist()
# print the list of tables
st.write(tables)

# Sidebar for customer selection
customer_names = [f"{customer['name'].lower()}_{customer['surname'].lower()}" for customer in customers]
selected_customer = st.sidebar.selectbox('Select a customer', customer_names)


if selected_customer:

    # Read data from the selected table
    query = f"SELECT * FROM {selected_customer}"
    df = pd.read_sql_query(query, conn)

    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Sidebar for feature selection
    feature_options = ['All'] + selected_features
    selected_feature = st.sidebar.selectbox('Select a feature to plot', feature_options)

    if selected_feature == 'All':
        for feature in selected_features:
            # Filter the DataFrame for the current feature
            feature_data = df[df['test_name'] == feature].sort_values('date')

            # Create and display the plot
            fig = px.scatter(feature_data, x='date', y='result', title=f'{feature} Over Time')
            fig.add_trace(px.line(feature_data, x='date', y='result').data[0])
            
            # Customize the layout
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Result",
                showlegend=False,
                xaxis=dict(
                    tickformat="%Y-%m-%d",
                    tickangle=45,
                )
            )
            
            # Update x-axis to show all dates
            fig.update_xaxes(tickmode='array', tickvals=feature_data['date'])
            
            st.plotly_chart(fig)
    else:
        # Filter the DataFrame for the selected feature
        feature_data = df[df['test_name'] == selected_feature]

        # Sort by date
        feature_data = feature_data.sort_values('date')

        # Plot the selected feature
        fig = px.scatter(feature_data, x='date', y='result', title=f'{selected_feature} Over Time')
        fig.add_trace(px.line(feature_data, x='date', y='result').data[0])
        
        # Customize the layout
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Result",
            showlegend=False,
            xaxis=dict(
                tickformat="%Y-%m-%d",
                tickangle=45,
            )
        )
        
        # Update x-axis to show all dates
        fig.update_xaxes(tickmode='array', tickvals=feature_data['date'])
        
        st.plotly_chart(fig)

        # Display summary statistics
        st.subheader(f'Summary Statistics for {selected_feature}')
        st.write(feature_data['result'].describe())

        # Display raw data
        st.subheader('Raw Data')
        st.dataframe(feature_data)

# Close the database connection
conn.close()