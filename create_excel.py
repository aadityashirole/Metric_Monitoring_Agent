import pandas as pd

# Define the sample dataset
data = {
    'Date': ['2026-08-01', '2026-08-01', '2026-08-02', '2026-08-02', '2026-08-03', '2026-08-03', '2026-08-04', '2026-08-04'],
    'Region': ['North', 'South', 'North', 'South', 'North', 'South', 'North', 'South'],
    'Product': ['Laptops', 'Laptops', 'Laptops', 'Laptops', 'Laptops', 'Laptops', 'Laptops', 'Laptops'],
    'Revenue': [5000, 3000, 5200, 3100, 4900, 2900, 2500, 3050]
}

# Save to Excel
df = pd.DataFrame(data)
df.to_excel('sales_data.xlsx', index=False)

print("✅ 'sales_data.xlsx' created successfully!")