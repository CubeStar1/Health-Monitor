import streamlit as st
import pandas as pd
import numpy as np
import serial
from serial.tools import list_ports
from PIL import Image
from utils import menu_with_redirect
import time
import streamviz


st.set_page_config(layout="wide")

def sensor_dashboard():
    if "data" not in st.session_state:
        st.session_state["data"] =  pd.DataFrame([[0.0,0.0, 0.0, 0.0]],columns=(["Heart Rate", "Temperature", "ECG", "SpO2"]))
    st.session_state["start"] = False
    with st.sidebar:
        with st.container(border=True):
            port_name = st.selectbox("Select PORT", [port.device for port in list_ports.comports()])
            try:
                arduino = serial.Serial(port=port_name, baudrate=9600)
                st.success("Arduino connected")
            except Exception as e:
                st.error(f"Stopped reading data from Arduino")

        with st.container(border=True):
            if st.button('Start', type="primary", use_container_width=True):
                st.session_state["start"] = True
                st.toast("Arduino started")


            if st.button('Stop', type="secondary", use_container_width=True):
                st.session_state["start"] = False
                st.toast("Arduino stopped")

            with st.popover("Save Data", use_container_width=True):

                st.session_state["data"].to_csv('sensor_data.csv', index=False)
                st.success("Data saved to sensor_data.csv")
                with open('sensor_data.csv', 'rb') as file:
                    st.download_button(label="Download CSV", data=file, file_name='sensor_data.csv', mime='text/csv')

            if st.button('Clear Data', use_container_width=True):
                st.session_state["data"] = pd.DataFrame([[0.0, 0.0, 0.0, 0.0]], columns=["Heart Rate", "Temperature", "ECG", "SpO2"])
                st.toast("Data cleared")


    st.markdown(
        """
        <style>
        .gradient-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 1rem 0;
            height: 10vh; /* Adjust height as needed */
            border-radius: 10px;
            background: linear-gradient(45deg, #ff6ec4, #7873f5);
        }

        .gradient-text {
            text-align: center;
            font-size: 2.5em;
            color: white;
        }
        </style>
        <div class="gradient-container">
            <h1 class="gradient-text">Sensor Dashboard</h1>
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
                    dataframe_widget = st.dataframe(df, use_container_width=True, hide_index=True)

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            line_chart_hr = st.line_chart(df["Heart Rate"], y = "Heart Rate", color="#ff3333")
        with st.container(border=True):
            line_chart_temp = st.line_chart(df["Temperature"], y= "Temperature")
    with col4:
        with st.container(border=True):
            line_chart_ecg = st.line_chart(df["ECG"], y = "ECG", color="#ff3333")
        with st.container(border=True):
            line_chart_spo2 = st.line_chart(df["SpO2"], y= "SpO2")

    if st.session_state["start"]:
        while True:
            try:
                line = arduino.readline().decode().strip()
                if line:
                    heart_rate, temperature, ecg, spo2 = map(float, line.split(','))
                    df2 = pd.DataFrame([[heart_rate, temperature, ecg, spo2]], columns=["Heart Rate", "Temperature", "ECG", "SpO2"])
                    st.session_state["data"] = pd.concat([st.session_state["data"], df2], ignore_index=True)
                    dataframe_widget.add_rows(df2)
                    line_chart_hr.add_rows(df2["Heart Rate"])
                    line_chart_temp.add_rows(df2["Temperature"])
                    line_chart_ecg.add_rows(df2["ECG"])
                    line_chart_spo2.add_rows(df2["SpO2"])

            except Exception as e:
                st.error(f"Error reading data from Arduino: {str(e)}")
                break

menu_with_redirect()
sensor_dashboard()
