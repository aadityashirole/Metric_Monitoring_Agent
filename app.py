import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from anomaly_engine import detect_rolling_anomalies

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(
    page_title="MetricGuard | Enterprise Anomaly Detection",
    page_icon="🛡️",
    layout="wide"
)

# ----------------- SESSION STATE MANAGEMENT -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"

if "companies_db" not in st.session_state:
    st.session_state.companies_db = {
        "admin@enterprise.com": {"password": "password123", "company": "Acme Global Corp"}
    }

# ----------------- VIEW 1: LANDING PAGE -----------------
def render_landing_page():
    st.caption("🛡️ ENTERPRISE METRIC GOVERNANCE")
    st.title("Autonomous Anomaly Detection for Data Pipelines")
    st.markdown(
        "Detect statistical deviations across multi-dimensional time-series metrics using adaptive "
        "rolling-window baselines and automated root-cause isolation."
    )
    
    # CTA Buttons
    cta_col1, cta_col2, _ = st.columns([1.2, 1.2, 3])
    with cta_col1:
        if st.button("🚀 Launch Instant Demo", use_container_width=True, type="primary"):
            st.session_state.authenticated = True
            st.session_state.company_name = "Global Logistics Inc."
            st.session_state.user_email = "demo@enterprise.com"
            st.rerun()
    with cta_col2:
        if st.button("Client Sign In", use_container_width=True):
            st.session_state.active_tab = "Login"
            st.rerun()

    st.divider()

    # Core Value Pillars using Native Native Clean Border Containers
    st.subheader("System Capabilities")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        with st.container(border=True):
            st.subheader("Adaptive Seasonality")
            st.write(
                "Applies moving 7-day rolling window Z-scores to filter out expected weekly cyclical "
                "dips without triggering false alarms."
            )
        
    with c2:
        with st.container(border=True):
            st.subheader("Root-Cause Isolation")
            st.write(
                "Hierarchically dissects high-variance days across regional and category segments to "
                "quantify baseline impact percentages."
            )
        
    with c3:
        with st.container(border=True):
            st.subheader("Zero-Noise Alerts")
            st.write(
                "Conditional guard clauses ensure executive incident summaries are dispatched via "
                "SMTP only when actionable anomalies occur."
            )

# ----------------- VIEW 2: AUTHENTICATION PORTAL -----------------
def render_auth_page():
    auth_col1, auth_col2, auth_col3 = st.columns([1, 1.5, 1])
    
    with auth_col2:
        st.subheader("🔐 Organization Portal Access")
        st.caption("Sign in or register your enterprise workspace.")
        
        tab_login, tab_register = st.tabs(["Sign In", "Register Organization"])

        with tab_login:
            st.write("")
            email = st.text_input("Work Email", placeholder="admin@enterprise.com")
            password = st.text_input("Password", type="password")
            st.write("")
            
            if st.button("Sign In", use_container_width=True, type="primary"):
                if email in st.session_state.companies_db and st.session_state.companies_db[email]["password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.company_name = st.session_state.companies_db[email]["company"]
                    st.rerun()
                else:
                    st.error("Invalid credentials. Use 'Launch Instant Demo' or check credentials.")

        with tab_register:
            st.write("")
            company = st.text_input("Organization Name", placeholder="e.g. Acme Corp")
            admin_email = st.text_input("Admin Email", placeholder="admin@domain.com")
            new_pass = st.text_input("Create Password", type="password")
            st.write("")
            
            if st.button("Create Organization Workspace", use_container_width=True, type="primary"):
                if company and admin_email and new_pass:
                    st.session_state.companies_db[admin_email] = {"password": new_pass, "company": company}
                    st.session_state.authenticated = True
                    st.session_state.user_email = admin_email
                    st.session_state.company_name = company
                    st.rerun()
                else:
                    st.warning("Please complete all required fields.")

        st.write("")
        if st.button("← Back to Overview", use_container_width=True):
            st.session_state.active_tab = "Home"
            st.rerun()

# ----------------- VIEW 3: ENTERPRISE DASHBOARD -----------------
def render_dashboard():
    # Header Bar
    h1, h2 = st.columns([3, 1])
    with h1:
        st.title(f"🏢 {st.session_state.company_name}")
        st.caption(f"Operator: `{st.session_state.user_email}` | Baseline Engine: **Rolling 7-Day Window**")
    with h2:
        st.write("")
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.active_tab = "Home"
            st.rerun()

    st.divider()

    # Sidebar Pipeline Controls
    st.sidebar.subheader("⚙️ Detection Parameters")
    window_size = st.sidebar.slider("Rolling Baseline Window (Days)", min_value=3, max_value=30, value=7)
    threshold = st.sidebar.slider("Statistical Threshold (σ)", min_value=1.5, max_value=4.0, value=2.8, step=0.1)

    st.sidebar.divider()
    st.sidebar.subheader("📂 Ingestion Target")
    uploaded_file = st.sidebar.file_uploader("Upload Metric Dataset (.xlsx)", type=['xlsx'])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_excel('sales_data.xlsx')

    # Run Anomaly Processing
    df_analyzed = detect_rolling_anomalies(df, window=window_size, threshold=threshold)
    anomalies = df_analyzed[df_analyzed['Is_Anomaly'] == True]

    # Clean KPI Cards
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Ingested Records", f"{len(df_analyzed):,}")
    kpi2.metric("Total Tracked Volume", f"${df_analyzed['Revenue'].sum():,.2f}")
    kpi3.metric(
        "Actionable Incidents", 
        f"{len(anomalies)}", 
        delta=f"{len(anomalies)} Flagged Incidents" if len(anomalies) > 0 else "All Clear", 
        delta_color="inverse"
    )

    st.divider()

    # Interactive Trajectory Graph
    st.subheader("Operational Metric Trajectory")
    
    selected_region = st.selectbox("Select Operational Region", options=sorted(df_analyzed['Region'].unique()))
    filtered_df = df_analyzed[df_analyzed['Region'] == selected_region]

    fig = px.line(
        filtered_df, 
        x='Date', 
        y='Revenue', 
        color='Category',
        labels={'Revenue': 'Revenue ($)', 'Date': 'Timeline'}
    )
    
    flagged_pts = filtered_df[filtered_df['Is_Anomaly'] == True]
    if not flagged_pts.empty:
        fig.add_trace(
            go.Scatter(
                x=flagged_pts['Date'],
                y=flagged_pts['Revenue'],
                mode='markers',
                marker=dict(size=10, color='#ef4444', symbol='circle'),
                name='Statistical Incident'
            )
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Incident Diagnostic Matrix
    st.subheader("Incident Diagnostic Breakdown")
    
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
        st.success("All metrics operating within normal baseline limits.")

# ----------------- MAIN ROUTER -----------------
def main():
    if not st.session_state.authenticated:
        if st.session_state.active_tab == "Home":
            render_landing_page()
        else:
            render_auth_page()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()