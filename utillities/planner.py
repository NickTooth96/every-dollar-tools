import json
import sys
import pandas as pd

DEBUG = False
BASE_ACCOUNT = "Staging Ground"

account_map = json.load(open("utillities/account-map.json", "r"))
accounts = account_map.keys()

def create_dataframe_from_csv(csv_path) -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_path)
        print(f"Data loaded successfully from {csv_path}") if DEBUG else None
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)
        
def make_title_friendly(string) -> str:
    return string.replace("-", " ").title()



def calculate_total_spent(df) -> dict:
    total_spent = {}
    for index, row in df.iterrows():
        group = row["Group"]
        category = row["Category"]
        amount = row["Amount"]
        if group not in total_spent:
                total_spent[group] = {f"{category}": amount}
        else:
            if category not in total_spent[group]:
                total_spent[group][f"{category}"] = amount
            else:
                total_spent[group][f"{category}"] += amount
    return total_spent

def make_printer_friendly(df):
    '''This function takes a dataframe and formats it in a way that is easy to read when printed. It returns a string representation of the dataframe.'''
    for index, row in df.iterrows():
        print(f"{row['Group']} -> {row['Category']}: {row['Amount']} from {row['From Account']}")

def plan_transfers(budget_df, transactions_df=None, checking_balance=None) -> dict:

    if transactions_df is not None:
        transactions_df["Category"] = transactions_df["Item"].apply(lambda x: x)
        calulated_totals = calculate_total_spent(transactions_df)
        print(calulated_totals)
    
    # for index, row in transactions_df.iterrows():
    #     print(row.to_dict())
        
    # for index, row in budget_df.iterrows():
    #     print(row.to_dict())
    
    
    sum_amounts = budget_df.groupby("from-account")["amount_float"].sum()
    print(sum_amounts) if DEBUG else None
    
    account_totals = {}
    for index, row in budget_df.iterrows():
        account = row['from-account']
        amount = row['amount_float']
        if account in account_totals:
            account_totals[account] += amount
        else:
            account_totals[account] = amount
            
    account_totals["checking"] -= checking_balance
    
    print(account_totals) if DEBUG else None
    planned_transfers = {}
        
    for account, total in account_totals.items():
        if account != "None":
            if account == "cash":
                print(f"Withdraw from [{BASE_ACCOUNT}]: ${total:.2f}")
            else:
                print(f"Transfer from [{BASE_ACCOUNT}] to [{make_title_friendly(account)}]: ${total:.2f}")
                
    return planned_transfers