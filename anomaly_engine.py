import pandas as pd
import numpy as np

def detect_rolling_anomalies(data_frame, window=7, threshold=2.5):
    """
    Computes rolling 7-day Z-scores grouped by Region and Category
    to prevent false positives from seasonality.
    """
    print(f"🧠 Running Rolling {window}-Day Window Anomaly Engine (Threshold: +/-{threshold}σ)...")
    
    df = data_frame.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by=['Region', 'Category', 'Date']).reset_index(drop=True)

    # 1. Group by dimensional segments (Region + Category)
    grouped = df.groupby(['Region', 'Category'])

    # 2. Calculate Rolling Mean & Standard Deviation over previous 'window' days
    df['Rolling_Mean'] = grouped['Revenue'].transform(lambda x: x.shift(1).rolling(window=window, min_periods=3).mean())
    df['Rolling_Std'] = grouped['Revenue'].transform(lambda x: x.shift(1).rolling(window=window, min_periods=3).std())

    # 3. Calculate Rolling Z-Score
    # Avoid zero division with safe numpy division
    std_safe = df['Rolling_Std'].replace(0, np.nan)
    df['Z_Score'] = (df['Revenue'] - df['Rolling_Mean']) / std_safe
    df['Z_Score'] = df['Z_Score'].fillna(0)

    # 4. Flag anomalies: True if Z-Score exceeds threshold
    df['Is_Anomaly'] = df['Z_Score'].abs() > threshold
    
    anomalies = df[df['Is_Anomaly'] == True]
    print(f"🚨 Detection Complete: Flagged {len(anomalies)} true anomalies out of {len(df)} records.")
    
    return df

if __name__ == "__main__":
    raw_df = pd.read_excel('sales_data.xlsx')
    results = detect_rolling_anomalies(raw_df, window=7, threshold=2.5)
    
    print("\n--- DETECTED PRODUCTION ANOMALIES ---")
    flagged = results[results['Is_Anomaly'] == True][['Date', 'Region', 'Category', 'Revenue', 'Rolling_Mean', 'Z_Score']]
    print(flagged)