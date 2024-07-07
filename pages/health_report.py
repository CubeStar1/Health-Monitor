import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import tempfile
from utils import menu_with_redirect

st.set_page_config(layout="wide")


class PDF(FPDF):
    def header(self):
        self.set_font('Times', 'B', 16)
        self.cell(0, 10, 'Health Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Times', 'B', 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Times', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_border(self):
        self.set_line_width(1)
        self.rect(5, 5, self.w - 10, self.h - 10)

    def add_table(self, data):
        self.set_font('Times', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(60, 10, 'Metric', 1, 0, 'C', 1)
        self.cell(60, 10, 'Value', 1, 1, 'C', 1)

        self.set_font('Times', '', 12)
        for key, value in data.items():
            self.cell(60, 10, key, 1)
            self.cell(60, 10, f"{value:.2f}", 1, 1)

    def add_image(self, path, x, y, w, h):
        self.image(path, x, y, w, h)


def generate_health_report(data):
    average_heart_rate = data["Heart Rate"].mean()
    average_temperature = data["Temperature"].mean()
    max_heart_rate = data["Heart Rate"].max()
    min_heart_rate = data["Heart Rate"].min()
    max_temperature = data["Temperature"].max()
    min_temperature = data["Temperature"].min()
    average_spO2 = data["SpO2"].mean()
    max_spO2 = data["SpO2"].max()
    min_spO2 = data["SpO2"].min()
    heart_rate_std = data["Heart Rate"].std()
    temperature_std = data["Temperature"].std()
    spO2_std = data["SpO2"].std()

    summary = {
        "Average Heart Rate": average_heart_rate,
        "Heart Rate Std Dev": heart_rate_std,
        "Average Temperature": average_temperature,
        "Temperature Std Dev": temperature_std,
        "Max Heart Rate": max_heart_rate,
        "Min Heart Rate": min_heart_rate,
        "Max Temperature": max_temperature,
        "Min Temperature": min_temperature,
        "Average SpO2": average_spO2,
        "SpO2 Std Dev": spO2_std,
        "Max SpO2": max_spO2,
        "Min SpO2": min_spO2
    }

    report_template = """
       Analysis:
       ---------
       - The average heart rate over the monitoring period was {Average Heart Rate:.2f} bpm.
         - Standard deviation: {Heart Rate Std Dev:.2f}
         - Maximum heart rate: {Max Heart Rate:.2f} bpm
         - Minimum heart rate: {Min Heart Rate:.2f} bpm

       - The average body temperature over the monitoring period was {Average Temperature:.2f} °C.
         - Standard deviation: {Temperature Std Dev:.2f}
         - Maximum temperature: {Max Temperature:.2f} °F
         - Minimum temperature: {Min Temperature:.2f} °F

       - The average SpO2 over the monitoring period was {Average SpO2:.2f} %.
         - Standard deviation: {SpO2 Std Dev:.2f}
         - Maximum SpO2: {Max SpO2:.2f} %
         - Minimum SpO2: {Min SpO2:.2f} %

       Rolling averages for heart rate, temperature, and SpO2 were calculated to analyze trends 
       over time. Significant deviations from these averages might indicate periods of increased 
       physical activity or potential health issues that warrant further investigation.

       Recommendations:
       ----------------
       - Maintain regular monitoring to ensure consistent heart rate, temperature, and SpO2.
       - Consult with a healthcare provider if there are significant anomalies or concerns.
       - Maintain a healthy lifestyle with a balanced diet, regular exercise, and adequate rest.

       Please remember that this report is based on the data provided and should not replace 
       professional medical advice.
       """

    return summary, report_template.format(**summary)


def plot_graphs(data):
    sns.set(style="whitegrid")
    fig, axs = plt.subplots(4, 1, figsize=(10, 20))

    sns.lineplot(data=data["Heart Rate"], ax=axs[0], color='r')
    axs[0].set_title('Heart Rate over Time')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Heart Rate (bpm)')

    sns.lineplot(data=data["Temperature"], ax=axs[1], color='b')
    axs[1].set_title('Temperature over Time')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Temperature (°C)')

    sns.lineplot(data=data["SpO2"], ax=axs[2], color='g')
    axs[2].set_title('SpO2 over Time')
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('SpO2 (%)')

    sns.heatmap(data[["Heart Rate", "Temperature", "SpO2", "ECG"]].corr(), annot=True, cmap='coolwarm', ax=axs[3])
    axs[3].set_title('Correlation Heatmap')

    plt.tight_layout()
    return fig


def save_report_to_pdf(report, summary, data, path):
    pdf = PDF()
    pdf.add_page()
    pdf.add_border()
    pdf.chapter_title("Health Report")
    pdf.chapter_body(report)
    pdf.add_page()
    pdf.add_border()
    pdf.chapter_title("Summary Table")
    pdf.add_table(summary)

    fig = plot_graphs(data)
    graph_path = "static/graphs.png"
    fig.savefig(graph_path)  # Increase DPI for higher resolution
    pdf.add_page()
    pdf.add_border()
    pdf.chapter_title("Graphs")
    pdf.add_image(graph_path, 10, 20, pdf.w - 20, pdf.h-20)  # Adjust height to maintain aspect ratio

    pdf.output(path)


menu_with_redirect()

st.markdown(
    """
    <style>
    .gradient-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 1rem 0;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(45deg, #ff6ec4, #7873f5);
        color: white;
        text-align: center;
    }
    .gradient-text {
        font-size: 2.5em;
        font-weight: bold;
    }
    .gradient-subtext {
        font-size: 1.2em;
        margin-top: 10px;
    }
    </style>
    <div class="gradient-container">
        <div class="gradient-text">Health Report</div>
        <div class="gradient-subtext">A comprehensive overview of your health data with detailed analysis and visualizations</div>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data = data.replace(0, np.nan)
    data = data.dropna()


    with st.popover("View Data", use_container_width=True):
        st.dataframe(data, use_container_width=True)

    summary, report = generate_health_report(data)
    # st.text_area("Generated Report", report, height=300)
    st.divider()
    st.markdown(report)

    if st.button("Download Report as PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            save_report_to_pdf(report, summary, data, tmp_file.name)
            st.success("Report generated successfully!")
            st.download_button(label="Download PDF", data=open(tmp_file.name, "rb"), file_name="health_report.pdf",
                               mime="application/pdf")