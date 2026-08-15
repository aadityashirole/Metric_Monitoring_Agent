import pandas as pd

def load_and_validate_metrics(filepath='sales_data.xlsx'):
    """
    Ingests raw Excel metric files and enforces schema data types.
    """
    try:
        df = pd.read_excel(filepath)
    except Exception as e:
        raise FileNotFoundError(f"❌ Error loading {filepath}: {e}")

    # Enforce Required Columns
    required_cols = ['Date', 'Region', 'Category', 'Revenue']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"❌ Ingestion Error: Missing required columns: {missing}")

    # Enforce Schema Types
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
    
    # Drop corrupted records
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        print(f"⚠️ Dropped {null_count} invalid/corrupted records during ingestion.")
        df = df.dropna().reset_index(drop=True)

    print(f"✅ Ingested and validated {len(df)} production records.")
    return df

if __name__ == "__main__":
    df = load_and_validate_metrics('sales_data.xlsx')
    print(df.head())