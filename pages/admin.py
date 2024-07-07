import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import plotly.express as px
from utils import menu_with_redirect

st.set_page_config(layout="wide")
menu_with_redirect()

# Function to check if the current user is an admin
def is_admin():
    return st.session_state.get('role') == 'admin'

# Function to fetch all users
def fetch_all_users():
    conn = sqlite3.connect('users.db')
    query = "SELECT id, username FROM users"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def fetch_all_user_data(user_id):
    conn = sqlite3.connect('users.db')
    query = """
    SELECT heart_rate AS 'Heart Rate', temperature AS Temperature, 
           ecg AS ECG, spo2 AS SpO2, timestamp
    FROM sensor_data 
    WHERE user_id = ?
    ORDER BY timestamp DESC
    LIMIT 100
    """
    print(f"Executing query: {query} with user_id: {user_id}")
    df = pd.read_sql_query(query, conn, params=(user_id,))
    print(f"Number of rows returned: {len(df)}")
    conn.close()
    return df
# Function to fetch user data from the database
def fetch_user_data(user_id, date):
    conn = sqlite3.connect('users.db')
    query = """
    SELECT heart_rate AS 'Heart Rate', temperature AS Temperature, 
           ecg AS ECG, spo2 AS SpO2, timestamp
    FROM sensor_data 
    WHERE user_id = ? 
    AND date(timestamp) = date(?)
    ORDER BY timestamp
    """
    date_str = date.isoformat()
    print(f"Executing query: {query} with user_id: {user_id} and date: {date_str}")
    df = pd.read_sql_query(query, conn, params=(user_id, date_str))
    print(f"Number of rows returned: {len(df)}")
    conn.close()
    return df
def users_with_data():
    conn = sqlite3.connect('users.db')
    query = """
    SELECT DISTINCT users.id, users.username, COUNT(sensor_data.id) as data_count
    FROM users
    LEFT JOIN sensor_data ON users.id = sensor_data.user_id
    GROUP BY users.id
    ORDER BY data_count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Check if user is admin
if not is_admin():
    st.error("Access denied. You must be an admin to view this page.")
    st.stop()

st.title("Admin Dashboard")

# Fetch all users
users = fetch_all_users()
st.subheader("Users with Data")
users_data = users_with_data()

with st.container(border=True):
    st.dataframe(users_data, use_container_width=True)



# User selection
with st.container(border=True):
    selected_user = st.selectbox("Select a user", users['username'], format_func=lambda x: f"User ID: {users[users['username'] == x]['id'].values[0]} - Username: {x}")

if selected_user:
    user_id = int(users[users['username'] == selected_user]['id'].values[0])

    with st.container(border=True):
        st.subheader(f"Data for user: {selected_user} (ID: {user_id})")

    # Date selection
        max_date = datetime.now().date()
        min_date = max_date - timedelta(days=30)
        selected_date = st.date_input("Select date for analysis", max_date, min_value=min_date, max_value=max_date)

    # Fetch data for the selected user and date
        data = fetch_user_data(user_id, selected_date)

    if not data.empty:
        # Display raw data
        st.subheader("Raw Data")
        st.dataframe(data, use_container_width=True)

        with st.container(border=True):
            st.subheader("Average Values")
            avg_values = data[["Heart Rate", "Temperature", "ECG", "SpO2"]].mean()
            st.write(f"Average Heart Rate: {avg_values['Heart Rate']:.2f} bpm")
            st.write(f"Average Temperature: {avg_values['Temperature']:.2f} °C")
            st.write(f"Average ECG: {avg_values['ECG']:.2f}")
            st.write(f"Average SpO2: {avg_values['SpO2']:.2f} %")

        with st.container(border=True):
            # Visualizations
            st.subheader("Visualizations")

            # Time series plots
            fig_hr = px.line(data['Heart Rate'], title='Heart Rate over Time')
            st.plotly_chart(fig_hr, use_container_width=True)

            fig_temp = px.line(data['Temperature'], title='Temperature over Time')
            st.plotly_chart(fig_temp, use_container_width=True)

            fig_ecg = px.line(data['ECG'], title='ECG over Time')
            st.plotly_chart(fig_ecg, use_container_width=True)

            fig_spo2 = px.line(data['SpO2'], title='SpO2 over Time')
            st.plotly_chart(fig_spo2, use_container_width=True)

    else:
        st.warning(f"No data available for user {selected_user} on {selected_date}.")

        # Additional debug information
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Check if user has any data at all
        cursor.execute("SELECT COUNT(*) FROM sensor_data WHERE user_id = ?", (user_id,))
        total_records = cursor.fetchone()[0]
        st.write(f"Debug: Total records for this user: {total_records}")

        # Get the date range of data for this user
        cursor.execute("SELECT MIN(date(timestamp)), MAX(date(timestamp)) FROM sensor_data WHERE user_id = ?",
                       (user_id,))
        date_range = cursor.fetchone()
        st.write(f"Debug: Data available from {date_range[0]} to {date_range[1]}")

        # Sample some actual data
        cursor.execute("SELECT * FROM sensor_data WHERE user_id = ? LIMIT 5", (user_id,))
        sample_data = cursor.fetchall()
        st.write("Debug: Sample of raw data from database:")
        for row in sample_data:
            st.write(row)

        conn.close()

else:
    st.info("Please select a user to view their data.")