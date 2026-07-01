import os
import sys
import argparse
import pandas as pd
from utillities.file import pdf_to_text, clean_text_file, make_budget_file_csv, parse_csv_download
from utillities.logging import file_info, initialize_log_file
from utillities.planner import plan_transfers, create_dataframe_from_csv
from utillities.utillities import audit_account_balance, assign_from_account, log_msg, Level
from utillities.settings import Settings


parser = argparse.ArgumentParser(description='Every Dollar Tools')
parser.add_argument('--transaction-file', type=str, help='Path to the input file (CSV format)')
parser.add_argument('--budget-file', type=str, help='Path to the monthly budget PDF file')
parser.add_argument('--budget-csv', type=str, help='Path to the monthly budget CSV file')
parser.add_argument('--plan-transfers', action='store_true', help='Plan transfers based on the budget and transactions')
parser.add_argument('--checking-balance', type=str, help='Current check balance')
# Add more argument --audit with required text value to specify which account to audit for balance
parser.add_argument('--audit', type=str, help='Specify which account to audit for balance')
parser.add_argument('--settings', type=str, help='Path to the settings file (JSON format)')

args = parser.parse_args()

output_dir = "output"
os.makedirs(output_dir, exist_ok=True) and log_msg("Creating output directory...", Level.INFO, file_info())
os.makedirs(f"{output_dir}/logs", exist_ok=True) and log_msg("Creating logs directory...", Level.INFO, file_info())


if args.settings:
    Settings().custom_settings(args.settings)
    log_msg(Settings().__dict__, Level.DEBUG, file_info())
    log_msg(f"Custom settings loaded from {args.settings}", Level.INFO, file_info())

if args.budget_file:
    filepath = os.path.expanduser(args.budget_file)
    basename = os.path.splitext(os.path.basename(filepath))[0]


    pdf_to_text(filepath, os.path.join(output_dir, f"{basename}.txt"))
    clean_text_file(os.path.join(output_dir, f"{basename}.txt"))
    make_budget_file_csv(os.path.join(output_dir, f"{basename}.txt.new"), os.path.join(output_dir, f"{basename}.csv"))
    os.remove(os.path.join(output_dir, f"{basename}.txt"))
    os.remove(os.path.join(output_dir, f"{basename}.txt.new"))

if args.transaction_file:
    transaction_df = create_dataframe_from_csv(args.transaction_file)
        
if args.budget_file:
    budget_df = create_dataframe_from_csv(f"output/{basename}.csv")
    budget_df["amount_float"] = budget_df[Settings().csv_key_map["Amount"]].apply(lambda x: float(x.replace("$", "").replace(",", "")))
    budget_df["from-account"] = budget_df.apply(assign_from_account, axis=1)
    log_msg(f'Assigned accounts to items in DataFrame', Level.INFO, file_info())

if args.budget_csv:
    filepath = os.path.expanduser(args.budget_csv)
    basename = os.path.splitext(os.path.basename(filepath))[0]
    Settings().set_csv_key_map({
        "Group": "Group",
        "Category": "Item",
        "Amount": "Planned",
        "Remaining": "Remaining"
    })
    parse_csv_download(args.budget_csv, f"output/{basename}.csv")
    budget_df = create_dataframe_from_csv(f"output/{basename}.csv")
    budget_df["amount_float"] = budget_df[Settings().csv_key_map["Amount"]].apply(lambda x: float(x))
    budget_df["from-account"] = budget_df.apply(assign_from_account, axis=1)
    log_msg(f'Assigned accounts to items in DataFrame', Level.INFO, file_info())
    
if args.checking_balance:
    checking_balance = float(args.checking_balance)
    log_msg(f"Using Checking account balance [$ß{args.checking_balance}]", Level.INFO, file_info())
else:
    checking_balance = float(0.00)
    log_msg(f"Using default Checking account balance [${float(0.00)}]", Level.INFO, file_info())

if args.plan_transfers:
    if not args.budget_file and not args.budget_csv :
        log_msg("The --budget-file argument is required to plan transfers.", Level.ERROR, file_info())
        sys.exit(1)
    else:
        if args.transaction_file:
            planned_transfers = plan_transfers(budget_df, transaction_df, checking_balance)
        else:
            planned_transfers = plan_transfers(budget_df, checking_balance=checking_balance)

if args.audit:
    audit_result = audit_account_balance(budget_df, args.audit)
    log_msg(f"Balance in [{args.audit}] (with buffer): ${audit_result:.2f}", Level.DISPLAY, file_info())