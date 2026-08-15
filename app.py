import streamlit as st
import pandas as pd
import plotly.express as px
from anomaly_engine import detect_rolling_anomalies

# Page Configuration
st.set_page_config(page_title="Metric Monitoring Agent", page_icon="📈", layout="wide")

st.title("🛡️ Enterprise Metric Anomaly Detection Agent")
st.markdown("Automated time-series monitoring pipeline utilizing **Rolling 7-Day Z-Score** statistics.")

# Sidebar Settings
st.sidebar.header("Engine Configuration")
window_size = st.sidebar.slider("Rolling Window (Days)", min_value=3, max_value=30, value=7)
threshold = st.sidebar.slider("Z-Score Sensitivity (σ)", min_value=1.5, max_value=4.0, value=2.5, step=0.1)

# File Loader / Local Data
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=['xlsx'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    df = pd.read_excel('sales_data.xlsx')

# Run Detection Engine
df_analyzed = detect_rolling_anomalies(df, window=window_size, threshold=threshold)
anomalies = df_analyzed[df_analyzed['Is_Anomaly'] == True]

# Top Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric("Total Records Processed", f"{len(df_analyzed):,}")
col2.metric("Total Revenue Tracked", f"${df_analyzed['Revenue'].sum():,.2f}")
col3.metric("Anomalies Flagged", f"{len(anomalies)}", delta=f"{len(anomalies)} critical" if len(anomalies) > 0 else "Normal", delta_color="inverse")

# Interactive Visualizations
st.subheader("Time-Series Metric Trajectory with Flagged Deviations")

# Segment selection
region_choice = st.selectbox("Select Region to Inspect", options=df_analyzed['Region'].unique())
filtered_data = df_analyzed[df_analyzed['Region'] == region_choice]

fig = px.line(
    filtered_data, 
    x='Date', 
    y='Revenue', 
    color='Category',
    title=f"Daily Revenue Trajectory - {region_choice} Region",
    labels={'Revenue': 'Daily Revenue ($)', 'Date': 'Date'}
)

# Highlight anomalies as red markers
filtered_anomalies = filtered_data[filtered_data['Is_Anomaly'] == True]
if not filtered_anomalies.empty:
    fig.add_scatter(
        x=filtered_anomalies['Date'], 
        y=filtered_anomalies['Revenue'], 
        mode='markers', 
        marker=dict(size=12, color='red', symbol='circle'), 
        name='Flagged Anomaly'
    )

st.plotly_chart(fig, use_container_width=True)

# Table of Flagged Incidents
st.subheader("🚨 Detected Incidents & Root-Cause Attributes")
if not anomalies.empty:
    st.dataframe(
        anomalies[['Date', 'Region', 'Category', 'Revenue', 'Rolling_Mean', 'Z_Score']].style.format({
            'Revenue': '${:,.2f}',
            'Rolling_Mean': '${:,.2f}',
            'Z_Score': '{:+.2f}σ'
        }),
        use_container_width=True
    )
else:
    st.success("No anomalies detected under current sensitivity threshold.")