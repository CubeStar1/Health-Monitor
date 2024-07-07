import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from utils import menu_with_redirect
st.set_page_config(layout="wide")
menu_with_redirect()


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
        <h1 class="gradient-text">Health Data Visualization Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data = data.drop(data.index[0])
    with st.popover("View Data", use_container_width=True):
        st.dataframe(data, use_container_width=True)
    with st.sidebar:
        with st.container(border=True):
            st.header("Visualizations")
            time_series = st.checkbox("Time Series", True)
            histograms = st.checkbox("Histograms", True)
            scatter_plots = st.checkbox("Scatter Plots", True)
            box_plots = st.checkbox("Box Plots", True)
            violin_plots = st.checkbox("Violin Plots", True)
            heatmap = st.checkbox("Heatmap", True)
            ecg_signal = st.checkbox("ECG Signal", True)

    if time_series:
        st.write("### Time Series Data")
        fig_hr = px.line(data, x=data.index, y="Heart Rate", title='Heart Rate over Time')
        st.plotly_chart(fig_hr, use_container_width=True)

        fig_temp = px.line(data, x=data.index, y="Temperature", title='Temperature over Time')
        st.plotly_chart(fig_temp, use_container_width=True)

        fig_spo2 = px.line(data, x=data.index, y="SpO2", title='SpO2 over Time')
        st.plotly_chart(fig_spo2, use_container_width=True)

    if histograms:
        st.write("### Distribution of Health Metrics")
        fig_hr_hist = px.histogram(data, x="Heart Rate", nbins=50, title='Heart Rate Distribution')
        st.plotly_chart(fig_hr_hist, use_container_width=True)

        fig_temp_hist = px.histogram(data, x="Temperature", nbins=50, title='Temperature Distribution')
        st.plotly_chart(fig_temp_hist, use_container_width=True)

        fig_spo2_hist = px.histogram(data, x="SpO2", nbins=50 , title='SpO2 Distribution')
        st.plotly_chart(fig_spo2_hist, use_container_width=True)
    if scatter_plots:
        st.write("### Relationship between Health Metrics")
        fig_hr_vs_temp = px.scatter(data, x="Heart Rate", y="Temperature", title='Heart Rate vs Temperature')
        st.plotly_chart(fig_hr_vs_temp, use_container_width=True)

        fig_hr_vs_spo2 = px.scatter(data, x="Heart Rate", y="SpO2", title='Heart Rate vs SpO2')
        st.plotly_chart(fig_hr_vs_spo2, use_container_width=True)

    if box_plots:
        st.write("### Distribution of Health Metrics")
        fig_box = px.box(data, y=["Heart Rate", "Temperature", "SpO2"], title='Box Plot of Health Metrics')
        st.plotly_chart(fig_box, use_container_width=True)

    if violin_plots:
        st.write("### Distribution of Health Metrics")
        fig_violin = px.violin(data, y=["Heart Rate", "Temperature", "SpO2"], title='Violin Plot of Health Metrics')
        st.plotly_chart(fig_violin, use_container_width=True)

    if heatmap:
        st.write("### Correlation Heatmap")
        correlation = data.corr()
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=correlation.values,
            x=correlation.columns,
            y=correlation.columns,
            colorscale='Viridis'
        ))
        fig_heatmap.update_layout(title='Correlation Heatmap')
        st.plotly_chart(fig_heatmap, use_container_width=True)

    if ecg_signal:
        st.write("### ECG Signal")
        fig_ecg = px.line(data, x=data.index, y="ECG", title='ECG Signal over Time')
        st.plotly_chart(fig_ecg, use_container_width=True)

