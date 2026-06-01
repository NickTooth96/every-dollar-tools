import os
import sys
import argparse
import pandas as pd
from utillities.file import pdf_to_text, clean_text_file, make_budget_file_csv
from utillities.planner import plan_transfers, create_dataframe_from_csv

parser = argparse.ArgumentParser(description='Every Dollar Tools')
parser.add_argument('--transaction-file', type=str, help='Path to the input file (CSV format)')
parser.add_argument('--budget-file', type=str, help='Path to the monthly budget PDF file')
parser.add_argument('--plan-transfers', action='store_true', help='Plan transfers based on the budget and transactions')
parser.add_argument('--checking-balance', type=str, help='Current check balance')

args = parser.parse_args()

if args.budget_file:
    filepath = os.path.expanduser(args.budget_file)
    basename, ext = os.path.splitext(filepath)

    pdf_to_text(args.budget_file, f"output/{basename}.txt")
    clean_text_file(f"output/{basename}.txt")
    make_budget_file_csv(f"output/{basename}.txt.new", f"output/{basename}.csv")
    os.remove(f"output/{basename}.txt")
    os.remove(f"output/{basename}.txt.new")

# Check if the --file argument is provided and read the data from the specified file into a DataFrame
if args.transaction_file:
    transaction_df = create_dataframe_from_csv(args.transaction_file)
        
if args.budget_file:
    budget_df = create_dataframe_from_csv(f"output/{basename}.csv")

if args.checking_balance:
    checking_balance = float(args.checking_balance)
else:
    checking_balance = float(0.00)

if args.plan_transfers:
    if not args.budget_file:
        print("The --budget-file argument is required to plan transfers.")
        sys.exit(1)
    else:
        if args.transaction_file:
            planned_transfers = plan_transfers(budget_df, transaction_df, checking_balance)
        else:
            planned_transfers = plan_transfers(budget_df, checking_balance=checking_balance)
