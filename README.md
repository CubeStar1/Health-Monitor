# Health Monitoring Dashboard

This repository contains the source code for a Health Monitoring Dashboard, designed to track and visualize vital health metrics in real-time. The project is built using Python, Streamlit, and SQLite, and it interfaces with Arduino sensors to collect health data.

## Features
- **Real-time Data Collection**: Collects data from health sensors connected to an Arduino, including heart rate, temperature, ECG, and SpO2.
- **Data Visualization**: Visualizes the collected data in real-time using Streamlit, providing insights into the user's health metrics.
- **Data Storage**: Stores the collected data in a SQLite database for historical analysis and review.
- **User Dashboard**: Offers a user-friendly dashboard for monitoring health metrics, including real-time charts and historical data analysis.
- **Generate Reports**: Generates reports based on the collected data, providing insights into the user's health trends and patterns.
- **Chatbot Integration**: Integrates a chatbot to provide health tips, reminders, and alerts based on the user's health metrics.
- **Customizable Alerts**: Sends customizable alerts and notifications based on the user's health metrics, helping them stay informed and proactive.

![Health Monitoring Dashboard](https://github.com/CubeStar1/Health-Monitor/blob/master/static/health-monitor-ui.jpg?raw=true)

## Installation

To set up the Health Monitoring Dashboard, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/CubeStar1/Health-Monitor.git
   cd Health-Monitor
    ```
2. **Install the Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
   
3. **Run the Application**

   ```bash
    streamlit run app.py
    ```
   
4. **Open the Application**

   Go to `http://localhost:8501` in your web browser to access the Health Monitoring Dashboard.

5. **Connect the Arduino Sensors**

   - Connect the health sensors to the Arduino board and ESP8266 module as per the wiring diagram provided in the `docs` folder.
   - Upload the `arduino_sensor_data.ino` sketch to the Arduino board to start collecting health data.
   - Upload the `esp8266.ino` sketch to the ESP8266 module to send the data to the Streamlit application.
   - Ensure that the Arduino is connected to the computer via USB and the ESP8266 is connected to the Wi-Fi network.
   - Update the IP address of the ESP8266 module in the `app.py` file to receive real-time data from the sensors.
   - Run the Streamlit application to start monitoring the health metrics in real-time.

## Usage

- **Health Monitor**: The main dashboard displays real-time health metrics, including heart rate, temperature, ECG, and SpO2. The user can view the data in the form of charts and graphs for better visualization.
- **Health Reports**: The user can generate health reports based on the collected data, providing insights into their health trends and patterns over time.
- **Chat with Health Assistant**: The chatbot integration allows the user to interact with a health assistant, who can provide health tips, reminders, and alerts based on the user's health metrics.
- **Data Visualiser**: The data visualizer tool allows the user to explore historical data, view trends, and analyze patterns in their health metrics.
- **Admin Panel**: The admin panel provides access to the database, allowing the user to manage and review the collected health data.
