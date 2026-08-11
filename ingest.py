import pandas as pd

# 1. Concept: Load Excel file into a Pandas DataFrame
print("📂 Reading Excel file...")
df = pd.read_excel('sales_data.xlsx')

# 2. Concept: Inspect data structure
print("\n--- FIRST 5 ROWS OF DATA ---")
print(df.head())

# 3. Concept: Data Validation Check (Ensure Revenue is numeric)
print("\n--- RUNNING DATA VALIDATION ---")
if 'Revenue' in df.columns:
    total_revenue = df['Revenue'].sum()
    avg_revenue = df['Revenue'].mean()
    print(f"✅ Revenue column found!")
    print(f"💰 Total Revenue: ${total_revenue}")
    print(f"📊 Average Daily Transaction: ${avg_revenue:.2f}")
else:
    print("❌ ERROR: Revenue column missing!")