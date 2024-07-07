import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from utils import menu_with_redirect
import sqlite3
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
menu_with_redirect()

# Function to fetch user data from the database
def fetch_user_data(user_id, date):
    conn = sqlite3.connect('users.db')
    query = """
    SELECT heart_rate AS 'Heart Rate', temperature AS Temperature, 
           ecg AS ECG, spo2 AS SpO2, timestamp
    FROM sensor_data 
    WHERE user_id = ? AND date(timestamp) = ?
    ORDER BY timestamp
    """
    df = pd.read_sql_query(query, conn, params=(user_id, date))
    conn.close()
    return df

# Check if user is logged in
if "user_id" not in st.session_state:
    st.error("Please log in to access the dashboard.")
    st.switch_page("app.py")

# Existing CSS styles
st.markdown(
    """
    <style>
    .main-container {
        padding: 20px;
        background: #f0f2f6;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .header {
        background: linear-gradient(90deg, #ff6ec4, #7873f5);
        color: white;
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .title {
        font-size: 2.5em;
        font-weight: bold;
    }
    .subtitle {
        font-size: 1.2em;
        margin-top: 10px;
    }
    .avg-container {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
    }
    .avg-box {
        flex: 1;
        background: linear-gradient(45deg, #6a11cb, #2575fc);
        color: white;
        padding: 20px;
        margin: 0 10px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5em;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown(
    """
    <div class="header">
        <div class="title">Health Data Visualization Dashboard</div>
        <div class="subtitle">Interactive visualizations of heart rate, temperature, ECG, and SpO2 data</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Date selector
max_date = datetime.now().date()
min_date = max_date - timedelta(days=30)  # Allow selection up to 30 days in the past
selected_date = st.date_input("Select date for analysis", max_date, min_value=min_date, max_value=max_date)

# Fetch data for the selected date
data = fetch_user_data(st.session_state.user_id, selected_date)

if not data.empty:
    # Calculate average values
    avg_heart_rate = data['Heart Rate'].mean()
    avg_temperature = data['Temperature'].mean()
    avg_ecg = data['ECG'].mean()
    avg_spo2 = data['SpO2'].mean()

    # Average value boxes
    st.markdown(
        f"""
        <div class="avg-container">
            <div class="avg-box">
                <div>Average Heart Rate</div>
                <div>{avg_heart_rate:.2f} bpm</div>
            </div>
            <div class="avg-box">
                <div>Average Temperature</div>
                <div>{avg_temperature:.2f} °F</div>
            </div>
            <div class="avg-box">
                <div>Average ECG</div>
                <div>{avg_ecg:.2f}</div>
            </div>
            <div class="avg-box">
                <div>Average SpO2</div>
                <div>{avg_spo2:.2f} %</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Plotly visualizations

    # 1. Line chart for Heart Rate
    fig_hr = px.line(data["Heart Rate"], title='Heart Rate over Time', color_discrete_sequence=['#FF5733'])

    # 2. Line chart for Temperature
    fig_temp = px.line(data['Temperature'], title='Temperature over Time', color_discrete_sequence=['#33CFFF'])

    # 3. Line chart for ECG
    fig_ecg = px.line(data['ECG'], title='ECG over Time', color_discrete_sequence=['#33FF57'])

    # 4. Line chart for SpO2
    fig_spo2 = px.line(data['SpO2'], title='SpO2 over Time', color_discrete_sequence=['#FF33A1'])

    # 5. Correlation heatmap
    corr = data[["Heart Rate", "Temperature", "ECG", "SpO2"]].corr()
    fig_corr = go.Figure(data=go.Heatmap(
                       z=corr.values,
                       x=corr.index.values,
                       y=corr.columns.values,
                       colorscale='Viridis'))
    fig_corr.update_layout(title='Correlation Heatmap')

    # 6. Histogram for Heart Rate
    fig_hr_hist = px.histogram(data, x='Heart Rate', title='Heart Rate Distribution', color_discrete_sequence=['#FF5733'])

    # 7. Histogram for Temperature
    fig_temp_hist = px.histogram(data, x='Temperature', title='Temperature Distribution', color_discrete_sequence=['#33CFFF'])

    # 8. Histogram for SpO2
    fig_spo2_hist = px.histogram(data, x='SpO2', title='SpO2 Distribution', color_discrete_sequence=['#FF33A1'])

    # 9. Scatter plot of Heart Rate vs. Temperature
    fig_hr_temp_scatter = px.scatter(data, x='Temperature', y='Heart Rate', title='Heart Rate vs Temperature', color_discrete_sequence=['#FF5733'])

    # 10. Box plot for each metric
    fig_box = px.box(data, y=['Heart Rate', 'Temperature', 'ECG', 'SpO2'], title='Box Plot for Health Metrics', color_discrete_sequence=['#FF5733', '#33CFFF', '#33FF57', '#FF33A1'])

    # Dashboard layout

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.plotly_chart(fig_hr, use_container_width=True)

        with st.container(border=True):
            st.plotly_chart(fig_temp, use_container_width=True)
    with col2:
        with st.container(border=True):
            st.plotly_chart(fig_ecg, use_container_width=True)

        with st.container(border=True):
            st.plotly_chart(fig_spo2, use_container_width=True)

    with st.container(border=True):
        st.plotly_chart(fig_corr, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        with st.container(border=True):
            st.plotly_chart(fig_hr_hist, use_container_width=True)

        with st.container(border=True):
            st.plotly_chart(fig_temp_hist, use_container_width=True)
    with col4:
        with st.container(border=True):
            st.plotly_chart(fig_spo2_hist, use_container_width=True)

        with st.container(border=True):
            st.plotly_chart(fig_hr_temp_scatter, use_container_width=True)

    with st.container(border=True):
        st.plotly_chart(fig_box, use_container_width=True)

else:
    st.warning(f"No data available for {selected_date}. Please select another date.")