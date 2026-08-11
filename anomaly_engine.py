import pandas as pd
from ingest import df # Importing our cleaned dataframe from ingest.py

def detect_anomalies(data_frame, threshold=1.5):
    print("🧠 RUNNING STATISTICAL ANOMALY ENGINE...")
    
    # 1. Calculate Mean and Standard Deviation of Revenue
    mean_rev = data_frame['Revenue'].mean()
    std_rev = data_frame['Revenue'].std()
    
    print(f"📊 Mean Revenue: ${mean_rev:.2f}")
    print(f"📉 Standard Deviation: ${std_rev:.2f}\n")
    
    # 2. Calculate Z-Score for every row
    # (Value - Mean) / Standard Deviation
    data_frame['Z_Score'] = (data_frame['Revenue'] - mean_rev) / std_rev
    
    # 3. Flag anomalies: True if Z-Score is beyond +threshold or -threshold
    data_frame['Is_Anomaly'] = data_frame['Z_Score'].abs() > threshold
    
    return data_frame

# --- EXECUTION ---
if __name__ == "__main__":
    results = detect_anomalies(df, threshold=1.5)
    
    print("--- ANOMALY DETECTION RESULTS ---")
    print(results[['Date', 'Region', 'Revenue', 'Z_Score', 'Is_Anomaly']])
    
    # Validation Check: Print flagged rows only
    anomalies = results[results['Is_Anomaly'] == True]
    print(f"\n🚨 TOTAL ANOMALIES FLAGGED: {len(anomalies)}")
    print(anomalies[['Date', 'Region', 'Revenue', 'Z_Score']])