import streamlit as st
import pandas as pd
import numpy as np
import serial
from serial.tools import list_ports
from PIL import Image
from utils import menu_with_redirect
import time
import streamviz
import sqlite3
from datetime import datetime
import requests
import altair as alt


ESP_IP_DEFAULT = "192.168.1.11"


st.set_page_config(layout="wide")


def store_sensor_data(user_id, heart_rate, temperature, ecg, spo2):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO sensor_data (user_id, heart_rate, temperature, ecg, spo2) VALUES (?, ?, ?, ?, ?)",
                  (user_id, heart_rate, temperature, ecg, spo2))
        conn.commit()
        print(f"Data saved for user {user_id}: HR={heart_rate}, Temp={temperature}, ECG={ecg}, SpO2={spo2}")
    except Exception as e:
        print(f"Error saving data: {e}")
    finally:
        conn.close()

def load_user_data(user_id):
    conn = sqlite3.connect('users.db')
    query = "SELECT heart_rate AS 'Heart Rate', temperature AS Temperature, ecg AS ECG, spo2 AS SpO2, timestamp FROM sensor_data WHERE user_id = ? ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df

def sensor_dashboard():
    if "user_id" not in st.session_state:
        st.error("Please log in to access the dashboard.")
        return

    user_id = st.session_state.user_id

    if "data" not in st.session_state:
        st.session_state["data"] = load_user_data(user_id)
        if st.session_state["data"].empty:
            st.session_state["data"] = pd.DataFrame([[0.0, 0.0, 0.0, 0.0, datetime.now()]],
                                                    columns=["Heart Rate", "Temperature", "ECG", "SpO2", "timestamp"])

    st.session_state["start"] = False
    st.session_state["timer"] = 30

    with st.sidebar:
        with st.container(border=True):
            ESP_IP = st.text_input("Enter ESP IP Address", ESP_IP_DEFAULT)
            time_duration = st.number_input("Set Timer", min_value=10, max_value=300, step=1, placeholder=30)
            try:
                st.success("Arduino connected")
            except Exception as e:
                st.error(f"Stopped reading data from Arduino")

        with st.container(border=True):
            if st.button('Start', type="primary", use_container_width=True):
                st.session_state["start"] = True
                st.session_state["timer"] = time_duration
                st.toast("Arduino started")

            if st.button('Stop', type="secondary", use_container_width=True):
                st.session_state["start"] = False
                st.toast("Arduino stopped")


            timer = st.empty()


            with st.popover("Save Data", use_container_width=True):
                st.session_state["data"].to_csv('sensor_data.csv', index=False)
                st.success("Data saved to sensor_data.csv")
                with open('sensor_data.csv', 'rb') as file:
                    st.download_button(label="Download CSV", data=file, file_name='sensor_data.csv', mime='text/csv')

            if st.button('Clear Data', use_container_width=True):
                st.session_state["data"] = pd.DataFrame([[0.0, 0.0, 0.0, 0.0, datetime.now()]],
                                                        columns=["Heart Rate", "Temperature", "ECG", "SpO2", "timestamp"])
                st.toast("Data cleared")

    st.markdown(
        """
        <style>
        .gradient-container-monitor {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin: 1rem 0;
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(45deg, #43cea2, #185a9d);
            color: white;
            text-align: center;
        }
        .gradient-text {
            font-size: 2.5em;
            font-weight: bold;
            font-family: 'Inter', sans-serif;
        }
        .gradient-subtext {
            font-size: 1.2em;
            margin-top: 10px;
        }
        </style>
        <div class="gradient-container-monitor">
            <div class="gradient-text">Health Monitor</div>
            <div class="gradient-subtext">Real-time tracking of your vital health metrics</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container(border=True, height=300):
        col1, col2 = st.columns(2)

        with col1:
            with st.container():
                with st.expander("Instructions", expanded=True):
                    st.markdown("- This dashboard reads data from an Arduino connected to the computer and displays it in real-time.")
                    st.markdown("- The data is displayed in a table on the right.")
                    st.markdown("- Click the 'Start' button to start reading data from the Arduino.")
                    st.markdown("- Click the 'Stop' button to stop reading data from the Arduino.")

        with col2:
            with st.container():
                with st.expander("Data Table", expanded=True):
                    df = st.session_state["data"]
                    dataframe_widget = st.dataframe(df[["Heart Rate", "Temperature", "ECG", "SpO2", "timestamp"]],
                                                    use_container_width=True, hide_index=True)

    col3, col4 = st.columns(2)

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            line_chart_hr = st.line_chart(st.session_state["data"]["Heart Rate"], y="Heart Rate", color="#FF5733")
        with st.container(border=True):
            line_chart_temp = st.line_chart(st.session_state["data"]["Temperature"], y="Temperature", color="#33FF57")
    with col4:
        with st.container(border=True):
            line_chart_ecg = st.line_chart(st.session_state["data"]["ECG"], y="ECG", color="#3357FF")
        with st.container(border=True):
            line_chart_spo2 = st.line_chart(st.session_state["data"]["SpO2"], y="SpO2", color="#FF33F1")

    if st.session_state["start"]:
        while st.session_state["timer"] > 0:
            try:
                response = requests.get(f"http://{ESP_IP}/data")

                if response.status_code == 200:
                    df_data = response.json()
                    heart_rate = float(df_data["heartRate"])
                    temperature = float(df_data["temperature"])
                    ecg = float(df_data["ecg"])
                    spo2 = float(df_data["spo2"])
                    current_time = datetime.now()
                    df2 = pd.DataFrame([[heart_rate, temperature, ecg, spo2, current_time]],
                                       columns=["Heart Rate", "Temperature", "ECG", "SpO2", "timestamp"])
                    st.session_state["data"] = pd.concat([st.session_state["data"], df2], ignore_index=True)
                    dataframe_widget.add_rows(df2)
                    line_chart_hr.add_rows(df2["Heart Rate"])
                    line_chart_temp.add_rows(df2["Temperature"])
                    line_chart_ecg.add_rows(df2["ECG"])
                    line_chart_spo2.add_rows(df2["SpO2"])

                    store_sensor_data(user_id, heart_rate, temperature, ecg, spo2)


                    st.session_state["timer"] -= 0.5
                    with timer:
                        st.write(f"Time remaining: {st.session_state['timer']} seconds")
                    time.sleep(0.1)

            except Exception as e:
                st.error(f"Error reading data from Arduino: {str(e)}")
                break


        st.session_state["start"] = False
        st.toast("Sensor reading completed")

menu_with_redirect()
sensor_dashboard()
