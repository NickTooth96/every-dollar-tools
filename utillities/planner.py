import sys
import pandas as pd

def plan_transfers(budget_csv_filepath, transactions_csv_filepath):
    budget_df = create_dataframe_from_csv(budget_csv_filepath)
    transactions_df = create_dataframe_from_csv(transactions_csv_filepath)

    planned_transfers = {}

    print(budget_df)
    print(transactions_df)
    
    return planned_transfers

def create_dataframe_from_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        print(f"Data loaded successfully from {csv_path}")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)