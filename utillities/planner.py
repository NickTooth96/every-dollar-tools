import json
import sys
import pandas as pd
from utillities.utillities import make_title_friendly, log_msg, log_variable, Level, Settings, file_info



def create_dataframe_from_csv(csv_path) -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_path)
        log_msg(f"Data loaded successfully from {csv_path}", Level.INFO, file_info())
        return df
    except Exception as e:
        log_msg(f"Error loading file: {e}", Level.ERROR, file_info())
        sys.exit(1)

def calculate_total_spent(df) -> dict:
    total_spent = {}
    for index, row in df.iterrows():
        group = row[Settings().csv_key_map["Group"]]
        category = row[Settings().csv_key_map["Category"]]
        amount = row[Settings().csv_key_map["Amount"]]
        if group not in total_spent:
                total_spent[group] = {f"{category}": amount}
        else:
            if category not in total_spent[group]:
                total_spent[group][f"{category}"] = amount
            else:
                total_spent[group][f"{category}"] += amount
    log_variable("total_spent", total_spent, Level.DEBUG, file_info())
    return total_spent

def make_printer_friendly(df):
    '''This function takes a dataframe and formats it in a way that is easy to read when printed. It returns a string representation of the dataframe.'''
    for index, row in df.iterrows():
        log_msg(f"{row['Group']} -> {row['Category']}: {row['Amount']} from {row['From Account']}", Level.DEBUG, file_info())

def plan_transfers(budget_df, transactions_df=None, checking_balance=None) -> dict:
    log_msg("Planning transfers...", Level.INFO, file_info())

    if transactions_df is not None:
        log_msg("Using transfers...", Level.INFO, file_info())
        transactions_df["Category"] = transactions_df["Item"].apply(lambda x: x)
        calulated_totals = calculate_total_spent(transactions_df)
        log_variable("calulated_totals", calulated_totals, Level.DEBUG, file_info())

    sum_amounts = budget_df.groupby("from-account")["amount_float"].sum()
    log_variable("sum_amounts", sum_amounts, Level.DEBUG, file_info())

    account_totals = {}
    for index, row in budget_df.iterrows():
        account = row['from-account']
        amount = row['amount_float']
        if account in account_totals:
            account_totals[account] += amount
        else:
            account_totals[account] = amount
        log_msg(f"Adding {amount} to {account}: total [{account_totals[account]}]", Level.DEBUG, file_info())
    
    log_variable("account_totals", account_totals, Level.DEBUG, file_info())     
    account_totals["checking"] -= checking_balance
    
    log_msg(f"Account totals: {account_totals}", Level.DEBUG, file_info())
    planned_transfers = {}
        
    for account, total in account_totals.items():
        if account != "None":
            if account == "cash":
                planned_transfers[account] = total
                log_msg(f"Withdraw from [{Settings().BASE_ACCOUNT}]: ${total:.2f}", Level.DISPLAY, file_info())
            else:
                planned_transfers[account] = total
                log_msg(f"Transfer from [{Settings().BASE_ACCOUNT}] to [{make_title_friendly(account)}]: ${total:.2f}", Level.DISPLAY, file_info())
    log_variable("planned_transfers", planned_transfers, Level.DEBUG, file_info())     
    return planned_transfers