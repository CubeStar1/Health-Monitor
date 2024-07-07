import streamlit as st
from utils import menu_with_redirect


def about_page():
    st.title("About Health Monitor")

    st.markdown(
        """
       - This app is designed to visualize health data collected from various sources such as heart rate monitors, body temperature sensors, ECG devices, and SpO2 monitors. 
       - It allows users to upload their CSV data files containing these metrics and provides interactive visualizations for better understanding and analysis.
        """
    )
    st.subheader("Key Features")
    st.markdown(
        """
        - Real-time visualization of health metrics including heart rate, temperature, SpO2, and ECG.
        - Multiple types of plots available: line charts, histograms, scatter plots, box plots, violin plots, heatmap, and ECG signal visualization.
        - Customizable color schemes and interactive components using Plotly and Streamlit.
        - Downloadable PDF health reports summarizing the collected data and providing insights.
        - Built-in AI chatbot for real-time health advice and monitoring.
        - User-friendly interface with options to clear data, save data, and view historical chats.
        """
    )

    st.subheader("Team Members")
    st.markdown(
        """
        - Avinash Anish: Lead Developer

        """
    )

    st.subheader("Contact Us")
    st.markdown(
        """
        
        Link to GitHub: [Avinash Anish](https://github.com/CubeStar1)

        """
    )


menu_with_redirect()
about_page()