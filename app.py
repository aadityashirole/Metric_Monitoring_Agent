import re
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

# ----------------- STRICT VALIDATION HELPERS -----------------
def validate_email(email_str: str) -> tuple[bool, str]:
    if not email_str or not email_str.strip():
        return False, "Email cannot be blank."
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email_str.strip()):
        return False, "Invalid email format (e.g. user@company.com)."
    return True, ""

def validate_company(name_str: str) -> tuple[bool, str]:
    cleaned = name_str.strip()
    if len(cleaned) < 3:
        return False, "Company name must be at least 3 characters long."
    return True, ""

def validate_password(pwd_str: str) -> tuple[bool, str]:
    if len(pwd_str) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Za-z]", pwd_str) or not re.search(r"[0-9]", pwd_str):
        return False, "Password must contain both letters and numbers."
    return True, ""

def validate_dataframe(df_to_check: pd.DataFrame) -> tuple[bool, str]:
    required_cols = {'Date', 'Region', 'Category', 'Revenue'}
    if not required_cols.issubset(df_to_check.columns):
        missing = required_cols - set(df_to_check.columns)
        return False, f"Missing required columns: {', '.join(missing)}"
    if df_to_check.empty:
        return False, "Uploaded file contains no records."
    return True, ""

# ----------------- SESSION STATE MANAGEMENT -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"
if "is_demo" not in st.session_state:
    st.session_state.is_demo = False
if "use_sample_data" not in st.session_state:
    st.session_state.use_sample_data = False

if "companies_db" not in st.session_state:
    st.session_state.companies_db = {
        "admin@enterprise.com": {"password": "Password123", "company": "Acme Global Corp"}
    }

# ----------------- VIEW 1: LANDING PAGE -----------------
def render_landing_page():
    st.caption("🛡️ ENTERPRISE METRIC GOVERNANCE")
    st.title("Autonomous Anomaly Detection for Data Pipelines")
    st.markdown(
        "Detect statistical deviations across multi-dimensional time-series metrics using adaptive "
        "rolling-window baselines and automated root-cause isolation."
    )
    
    cta_col1, cta_col2, _ = st.columns([1.2, 1.2, 3])
    with cta_col1:
        if st.button("🚀 Launch Instant Demo", use_container_width=True, type="primary"):
            st.session_state.authenticated = True
            st.session_state.company_name = "Global Logistics Demo Corp"
            st.session_state.user_email = "demo@enterprise.com"
            st.session_state.is_demo = True
            st.session_state.use_sample_data = True
            st.rerun()
    with cta_col2:
        if st.button("Client Sign In", use_container_width=True):
            st.session_state.active_tab = "Login"
            st.rerun()

    st.divider()

    st.subheader("System Capabilities")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        with st.container(border=True):
            st.subheader("Adaptive Seasonality")
            st.write("Applies moving 7-day rolling window Z-scores to filter out expected weekly cyclical dips without false alarms.")
        
    with c2:
        with st.container(border=True):
            st.subheader("Root-Cause Isolation")
            st.write("Hierarchically dissects high-variance days across regional and category segments to quantify baseline impact percentages.")
        
    with c3:
        with st.container(border=True):
            st.subheader("Zero-Noise Alerts")
            st.write("Conditional guard clauses ensure executive incident summaries are dispatched via SMTP only when actionable anomalies occur.")

# ----------------- VIEW 2: AUTHENTICATION PORTAL -----------------
def render_auth_page():
    auth_col1, auth_col2, auth_col3 = st.columns([1, 1.5, 1])
    
    with auth_col2:
        st.subheader("🔐 Organization Portal Access")
        st.caption("Sign in or register your enterprise workspace.")
        
        tab_login, tab_register = st.tabs(["Sign In", "Register Organization"])

        with tab_login:
            st.write("")
            with st.form("login_form"):
                email = st.text_input("Work Email", placeholder="admin@enterprise.com")
                password = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Sign In", use_container_width=True, type="primary")

                if submit_login:
                    email_ok, email_msg = validate_email(email)
                    if not email_ok:
                        st.error(f"⚠️ {email_msg}")
                    elif email not in st.session_state.companies_db:
                        st.error("⚠️ Workspace not found. Please register an organization first.")
                    elif st.session_state.companies_db[email]["password"] != password:
                        st.error("⚠️ Incorrect password.")
                    else:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.company_name = st.session_state.companies_db[email]["company"]
                        st.session_state.is_demo = False
                        st.session_state.use_sample_data = False
                        st.rerun()

        with tab_register:
            st.write("")
            with st.form("register_form"):
                company = st.text_input("Organization Name", placeholder="e.g. Acme Corp (Min 3 chars)")
                admin_email = st.text_input("Admin Work Email", placeholder="admin@domain.com")
                new_pass = st.text_input("Create Password", type="password", help="Min 8 chars with letters & numbers")
                submit_reg = st.form_submit_button("Create Organization Workspace", use_container_width=True, type="primary")

                if submit_reg:
                    comp_ok, comp_msg = validate_company(company)
                    email_ok, email_msg = validate_email(admin_email)
                    pwd_ok, pwd_msg = validate_password(new_pass)

                    if not comp_ok:
                        st.error(f"⚠️ {comp_msg}")
                    elif not email_ok:
                        st.error(f"⚠️ {email_msg}")
                    elif not pwd_ok:
                        st.error(f"⚠️ {pwd_msg}")
                    elif admin_email in st.session_state.companies_db:
                        st.error("⚠️ An organization is already registered under this email.")
                    else:
                        st.session_state.companies_db[admin_email] = {
                            "password": new_pass, 
                            "company": company.strip()
                        }
                        st.session_state.authenticated = True
                        st.session_state.user_email = admin_email
                        st.session_state.company_name = company.strip()
                        st.session_state.is_demo = False
                        st.session_state.use_sample_data = False
                        st.rerun()

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
        st.caption(f"Operator: `{st.session_state.user_email}` | Engine: **Adaptive Rolling 7-Day Z-Score**")
    with h2:
        st.write("")
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.company_name = ""
            st.session_state.user_email = ""
            st.session_state.active_tab = "Home"
            st.session_state.is_demo = False
            st.session_state.use_sample_data = False
            st.rerun()

    st.divider()

    # Sidebar Pipeline Controls
    st.sidebar.subheader("⚙️ Detection Parameters")
    window_size = st.sidebar.slider("Rolling Baseline Window (Days)", min_value=3, max_value=30, value=7)
    threshold = st.sidebar.slider("Statistical Threshold (σ)", min_value=1.5, max_value=4.0, value=2.8, step=0.1)

    st.sidebar.divider()
    st.sidebar.subheader("📂 Ingestion Target")
    uploaded_file = st.sidebar.file_uploader("Upload Metric Dataset (.xlsx)", type=['xlsx'])

    # Determine Data Source
    df = None
    if uploaded_file is not None:
        try:
            temp_df = pd.read_excel(uploaded_file)
            is_valid, err_msg = validate_dataframe(temp_df)
            if is_valid:
                df = temp_df
            else:
                st.sidebar.error(f"Schema Error: {err_msg}")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")
    elif st.session_state.use_sample_data:
        df = pd.read_excel('sales_data.xlsx')

    # EMPTY WORKSPACE STATE (If no data uploaded yet)
    if df is None:
        st.info("👋 **Welcome to your new workspace!** Your data pipeline is currently idle.")
        with st.container(border=True):
            st.subheader("📥 Ingest Telemetry Data to Begin")
            st.markdown(
                "Upload your organization's time-series Excel file (`.xlsx`) via the sidebar or load "
                "our enterprise benchmark dataset to test the detection engine."
            )
            st.caption("Required columns: `Date` (YYYY-MM-DD), `Region`, `Category`, `Revenue`")
            st.write("")
            if st.button("📊 Load Sample Benchmark Dataset", type="primary"):
                st.session_state.use_sample_data = True
                st.rerun()
        return

    # DATA INGESTED: RUN ENGINE & RENDER DASHBOARD
    df_analyzed = detect_rolling_anomalies(df, window=window_size, threshold=threshold)
    anomalies = df_analyzed[df_analyzed['Is_Anomaly'] == True]

    # KPI Cards
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