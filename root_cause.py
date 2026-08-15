import pandas as pd
from anomaly_engine import detect_rolling_anomalies

def run_root_cause_matrix(data_frame, window=7, threshold=2.5):
    # 1. Detect rolling anomalies
    df_results = detect_rolling_anomalies(data_frame, window=window, threshold=threshold)
    anomalies = df_results[df_results['Is_Anomaly'] == True]

    if anomalies.empty:
        print("✅ No statistical anomalies found. Skipping root cause analysis.")
        return anomalies

    print("\n🔍 --- MULTI-DIMENSIONAL ROOT-CAUSE BREAKDOWN ---")
    
    # 2. Iterate through each flagged record
    for _, row in anomalies.iterrows():
        date_str = pd.to_datetime(row['Date']).strftime('%Y-%m-%d')
        region = row['Region']
        category = row['Category']
        actual = row['Revenue']
        expected = row['Rolling_Mean']
        z_score = row['Z_Score']
        
        # Calculate divergence
        diff = actual - expected
        pct_change = (diff / expected) * 100
        direction = "SPIKE 📈" if diff > 0 else "CRASH 📉"

        print(f"\n🚨 Incident Date: {date_str}")
        print(f"   • Dimension: Region [{region}] | Category [{category}]")
        print(f"   • Behavior: {direction}")
        print(f"   • Actual Recorded: ${actual:,.2f}")
        print(f"   • 7-Day Baseline (Expected): ${expected:,.2f}")
        print(f"   • Variance: {pct_change:+.1f}% ({z_score:+.2f}σ deviation)")
        
    return anomalies

if __name__ == "__main__":
    raw_df = pd.read_excel('sales_data.xlsx')
    run_root_cause_matrix(raw_df)