import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_production_data():
    np.random.seed(42)
    
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(180)] # 6 months of daily data
    regions = ['North', 'South', 'East', 'West']
    categories = ['Electronics', 'Home Appliances', 'Clothing']

    rows = []
    for d in dates:
        # Day-of-week seasonality multiplier (Weekends lower)
        day_factor = 0.7 if d.weekday() >= 5 else 1.0
        
        for r in regions:
            for c in categories:
                # Base volume per category
                base = 4000 if c == 'Electronics' else (2500 if c == 'Home Appliances' else 1200)
                
                # Normal random variance (+/- 10%)
                noise = np.random.normal(0, base * 0.08)
                revenue = round(max((base * day_factor) + noise, 300), 2)
                
                # Injected Critical Anomalies for testing
                # 1. Flash crash in North Electronics on 2025-03-15
                if d == datetime(2025, 3, 15) and r == 'North' and c == 'Electronics':
                    revenue = 650.00
                
                # 2. Huge spike in West Clothing on 2025-05-10
                if d == datetime(2025, 5, 10) and r == 'West' and c == 'Clothing':
                    revenue = 4800.00
                
                rows.append({
                    'Date': d.strftime('%Y-%m-%d'),
                    'Region': r,
                    'Category': c,
                    'Revenue': revenue
                })

    df = pd.DataFrame(rows)
    df.to_excel('sales_data.xlsx', index=False)
    print(f"✅ Generated {len(df)} rows across {len(dates)} days into 'sales_data.xlsx'!")

if __name__ == "__main__":
    generate_production_data()