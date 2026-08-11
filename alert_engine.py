import smtplib
from email.mime.text import MIMEText
import pandas as pd
from anomaly_engine import detect_anomalies
from ingest import df

# 1. NEW: Real Email Sending Function
def send_real_email(subject, body, to_email):
    # Sender Configuration (Use your real Gmail address and App Password)
    sender_email = "your_email@gmail.com"
    app_password = "YOUR_APP_PASSWORD_HERE"  # Generated via Google Account -> Security -> App Passwords
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"✅ Real email successfully sent to {to_email}!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# 2. Main Alert Handler
def send_anomaly_alert(data_frame, threshold=1.5):
    # Convert Date column to datetime safety check
    data_frame['Date'] = pd.to_datetime(data_frame['Date'])
    
    # Detect Anomalies
    results = detect_anomalies(data_frame, threshold)
    anomalies = results[results['Is_Anomaly'] == True]
    
    # ZERO-NOISE GUARD CLAUSE
    if anomalies.empty:
        print("\n🟢 STATUS: Normal business metrics detected. Zero emails sent (Zero-Noise Policy).")
        return
    
    print("\n🚨 ANOMALY DETECTED! PREPARING EXECUTIVE EMAIL ALERT...")
    
    # Construct Email Payload & Send
    for idx, row in anomalies.iterrows():
        anomaly_date = pd.to_datetime(row['Date']).strftime('%Y-%m-%d')
        region = row['Region']
        actual_rev = row['Revenue']
        
        # Historical stats
        historical = data_frame[(data_frame['Region'] == region) & (data_frame['Date'] != row['Date'])]
        hist_avg = historical['Revenue'].mean()
        drop_pct = ((hist_avg - actual_rev) / hist_avg) * 100

        subject_line = f"🚨 Metric Drop Alert: {region} Region ({anomaly_date})"
        
        email_content = f"""Dear Business Team,

An automated anomaly check flagged a critical metric divergence in your Excel data.

SUMMARY OF FINDINGS:
------------------------------------------------------------------------
• Incident Date: {anomaly_date}
• Metric Monitored: Revenue
• Affected Segment: {region} Region
• Recorded Value: ${actual_rev}
• Normal Expected Average: ${hist_avg:.2f}
• Divergence Impact: -{drop_pct:.1f}% drop below baseline

ACTION REQUIRED:
Please review payment logs or regional inventory for {region} on {anomaly_date}.

-- 
Automated Metric Monitoring Agent (Python / Pandas Engine)
"""
        # Print preview to terminal
        print(f"\nSending alert for {region}...")
        
        # 3. CALL REAL EMAIL FUNCTION HERE
        # Replace 'executive_team@company.com' with your destination email address
        send_real_email(subject_line, email_content, "destination_email@example.com")

# --- EXECUTION ---
if __name__ == "__main__":
    send_anomaly_alert(df, threshold=1.5)