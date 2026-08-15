import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from anomaly_engine import detect_rolling_anomalies

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(
    page_title="MetricGuard | Enterprise Anomaly Detection",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- GLOBAL ENTERPRISE STYLING (CSS) -----------------
st.markdown("""
<style>
    /* Global Typography & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean Enterprise Cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 16px;
    }
    
    .pricing-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 20px;
        height: 100%;
    }
    
    .badge-primary {
        background-color: #eff6ff;
        color: #1d4ed8;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .badge-danger {
        background-color: #fef2f2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Sleek Buttons */
    div.stButton > button {
        border-radius: 6px;
        font-weight: 500;
        border: 1px solid #cbd5e1;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        border-color: #0f172a;
        color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE MANAGEMENT -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"

# Mock Enterprise DB
if "companies_db" not in st.session_state:
    st.session_state.companies_db = {
        "admin@enterprise.com": {"password": "password123", "company": "Acme Global Corp"}
    }

# ----------------- VIEW 1: CLEAN LANDING PAGE -----------------
def render_landing_page():
    # Hero Section
    st.markdown("<br>", unsafe_allow_html=True)
    hero_col1, hero_col2 = st.columns([3, 1])
    with hero_col1:
        st.markdown("<span class='badge-primary'>ENTERPRISE METRIC GOVERNANCE</span>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 2.75rem; font-weight: 700; color: #0f172a; margin-top: 10px;'>Autonomous Anomaly Detection for Data Pipelines</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.15rem; color: #64748b; line-height: 1.6;'>Detect statistical deviations across multi-dimensional time-series data using adaptive rolling-window baselines and automated root-cause isolation.</p>", unsafe_allow_html=True)
    
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

    st.markdown("<br><hr style='border: none; border-top: 1px solid #e2e8f0;'><br>", unsafe_allow_html=True)

    # Core Value Pillars
    st.markdown("<h3 style='color: #0f172a; font-weight: 600;'>System Capabilities</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #0f172a; margin-top: 0;'>Adaptive Seasonality</h4>
            <p style='color: #64748b; font-size: 0.95rem; margin-bottom: 0;'>
                Applies moving 7-day rolling window Z-scores to filter out expected weekly cyclical dips without false alarms.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #0f172a; margin-top: 0;'>Root-Cause Isolation</h4>
            <p style='color: #64748b; font-size: 0.95rem; margin-bottom: 0;'>
                Hierarchically dissects high-variance days across regional and category segments to compute percentage baseline impact.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #0f172a; margin-top: 0;'>Zero-Noise SMTP Alerts</h4>
            <p style='color: #64748b; font-size: 0.95rem; margin-bottom: 0;'>
                Conditional guard clauses ensure email digests are triggered exclusively when statistically critical incidents occur.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ----------------- VIEW 2: AUTHENTICATION PORTAL -----------------
def render_auth_page():
    st.markdown("<br>", unsafe_allow_html=True)
    auth_col1, auth_col2, auth_col3 = st.columns([1, 1.5, 1])
    
    with auth_col2:
        st.markdown("<h2 style='text-align: center; color: #0f172a; font-weight: 600;'>Workspace Access</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.95rem;'>Sign in or register your organization's monitoring environment.</p>", unsafe_allow_html=True)
        st.write("")

        tab_login, tab_register = st.tabs(["Sign In", "Register Organization"])

        with tab_login:
            st.write("")
            email = st.text_input("Work Email", placeholder="name@company.com")
            password = st.text_input("Password", type="password")
            st.write("")
            
            if st.button("Sign In", use_container_width=True, type="primary"):
                if email in st.session_state.companies_db and st.session_state.companies_db[email]["password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.company_name = st.session_state.companies_db[email]["company"]
                    st.rerun()
                else:
                    st.error("Invalid credentials. Enter valid email/password or use 'Launch Instant Demo'.")

        with tab_register:
            st.write("")
            company = st.text_input("Organization Name", placeholder="e.g. Stripe, Acme Corp")
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

# ----------------- VIEW 3: ENTERPRISE DASHBOARD -----------------
def render_dashboard():
    # Top Header
    h1, h2 = st.columns([3, 1])
    with h1:
        st.markdown(f"<h2 style='margin: 0; color: #0f172a;'>{st.session_state.company_name}</h2>", unsafe_allow_html=True)
        st.caption(f"Active User: `{st.session_state.user_email}` | Pipeline Engine: **Rolling 7-Day Z-Score**")
    with h2:
        st.write("")
        if st.button("Log Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.active_tab = "Home"
            st.rerun()

    st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 12px 0 24px 0;'>", unsafe_allow_html=True)

    # Sidebar Pipeline Controls
    st.sidebar.markdown("### ⚙️ Pipeline Controls")
    window_size = st.sidebar.slider("Rolling Window (Days)", min_value=3, max_value=30, value=7)
    threshold = st.sidebar.slider("Statistical Threshold (σ)", min_value=1.5, max_value=4.0, value=2.8, step=0.1)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📂 Data Ingestion")
    uploaded_file = st.sidebar.file_uploader("Upload Transaction Dataset (.xlsx)", type=['xlsx'])

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
    kpi2.metric("Total Revenue Volume", f"${df_analyzed['Revenue'].sum():,.2f}")
    kpi3.metric(
        "Actionable Incidents", 
        f"{len(anomalies)}", 
        delta=f"{len(anomalies)} Flagged Deviations" if len(anomalies) > 0 else "All Normal", 
        delta_color="inverse"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Trajectory Graph
    st.markdown("<h4 style='color: #0f172a; margin-bottom: 4px;'>Operational Metric Trajectory</h4>", unsafe_allow_html=True)
    st.caption("Inspect daily transaction trajectories across regional divisions and isolated anomalies.")
    
    selected_region = st.selectbox("Select Dimension Region", options=sorted(df_analyzed['Region'].unique()))
    filtered_df = df_analyzed[df_analyzed['Region'] == selected_region]

    # Enterprise Plotly Chart Theme (Subtle Grays / Minimal Lines)
    fig = px.line(
        filtered_df, 
        x='Date', 
        y='Revenue', 
        color='Category',
        color_discrete_sequence=['#2563eb', '#64748b', '#0891b2'],
        labels={'Revenue': 'Revenue ($)', 'Date': 'Timeline'}
    )
    
    # Highlight Anomalies
    flagged_pts = filtered_df[filtered_df['Is_Anomaly'] == True]
    if not flagged_pts.empty:
        fig.add_trace(
            go.Scatter(
                x=flagged_pts['Date'],
                y=flagged_pts['Revenue'],
                mode='markers',
                marker=dict(size=10, color='#dc2626', symbol='circle'),
                name='Statistical Incident'
            )
        )

    fig.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Inter", color="#334155"),
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Incident Diagnostic Matrix
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #0f172a;'>Incident Diagnostic Breakdown</h4>", unsafe_allow_html=True)
    
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
        st.info("No statistical deviations detected for the configured threshold.")

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