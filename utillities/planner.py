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

def assign_from_account(row) -> str:
    '''This function takes a row from the budget dataframe and checks the group and category against the account map to determine which account the transfer should be made from. It returns the account name as a string.'''
    check_group = row["Group"].lower()
    check_catagory = row["Category"].lower()
    # the account map is a json dictionary structured like this: account_map = {
    #        "Account": {
    #            "Group": [ 
    #               "category1",
    #               "category2" ]
    #        }
    #    }
    for account, group_catagories in account_map.items():
        print(f"Account: {account} group_catagories: {group_catagories}") if DEBUG else None
        for group, catagories in group_catagories.items():
            print(f"Group: {group} catagories: {catagories}") if DEBUG else None
            if check_group == group.lower():
                print(f"!!! Group match found: {group}") if DEBUG else None
                for catagory in catagories:
                    if check_catagory == catagory.lower():
                        print(f"!!! Category match found: {catagory}") if DEBUG else None
                        return account        
    return "None"

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

def plan_transfers(budget_df, transactions_df=None) -> dict:
    budget_df["amount_float"] = budget_df["Amount"].apply(lambda x: float(x.replace("$", "").replace(",", "")))
    budget_df["from-account"] = budget_df.apply(assign_from_account, axis=1)
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

    print(account_totals) if DEBUG else None
    planned_transfers = {}
        
    for account, total in account_totals.items():
        if account != "None":
            if account == "cash":
                print(f"Withdraw from [{BASE_ACCOUNT}]: ${total:.2f}")
            else:
                print(f"Transfer from [{BASE_ACCOUNT}] to [{make_title_friendly(account)}]: ${total:.2f}")
                
    return planned_transfers