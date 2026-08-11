import pandas as pd
from anomaly_engine import detect_anomalies
from ingest import df

def analyze_root_cause(data_frame, threshold=1.5):
    # Ensure Date column is explicitly converted to datetime
    data_frame['Date'] = pd.to_datetime(data_frame['Date'])
    
    # 1. Run Anomaly Engine
    results = detect_anomalies(data_frame, threshold)
    anomalies = results[results['Is_Anomaly'] == True]
    
    if anomalies.empty:
        print("✅ No anomalies detected. Root-cause analysis skipped.")
        return None

    print("\n🔍 RUNNING ROOT-CAUSE ANALYSIS...")
    
    # 2. Iterate through each detected anomaly
    for idx, row in anomalies.iterrows():
        anomaly_date = row['Date']
        anomaly_region = row['Region']
        actual_rev = row['Revenue']
        
        # Calculate historical average for this specific region (excluding anomaly date)
        historical_data = data_frame[(data_frame['Region'] == anomaly_region) & (data_frame['Date'] != anomaly_date)]
        historical_avg = historical_data['Revenue'].mean()
        
        # Percentage Drop Calculation
        drop_pct = ((historical_avg - actual_rev) / historical_avg) * 100
        
        # Format date cleanly using pd.to_datetime safety check
        formatted_date = pd.to_datetime(anomaly_date).strftime('%Y-%m-%d')
        
        print(f"\n🚨 ANOMALY INSIGHT DETECTED:")
        print(f" 📍 Date: {formatted_date}")
        print(f" 📍 Affected Region: {anomaly_region}")
        print(f" 📉 Actual Revenue: ${actual_rev}")
        print(f" 📊 Historical Regional Average: ${historical_avg:.2f}")
        print(f" ⚠️ Impact: Revenue dropped by {drop_pct:.1f}% below normal levels in {anomaly_region}!")

# --- EXECUTION ---
if __name__ == "__main__":
    analyze_root_cause(df, threshold=1.5)