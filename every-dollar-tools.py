import os
import sys
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Every Dollar Tools')
parser.add_argument('--transaction-file', type=str, help='Path to the input file (CSV format)')
parser.add_argument('--budget', type=str, help='Path to the monthly budget PDF file')

args = parser.parse_args()

if args.budget:
    from utillities.file import pdf_to_text, clean_text_file, make_budget_file_csv
    filepath = os.path.expanduser(args.budget)
    basename, ext = os.path.splitext(filepath)

    pdf_to_text(args.budget, f"output/{basename}.txt")
    clean_text_file(f"output/{basename}.txt")
    make_budget_file_csv(f"output/{basename}.txt.new", f"output/{basename}.csv")
    os.remove(f"output/{basename}.txt")
    os.remove(f"output/{basename}.txt.new")

# Check if the --file argument is provided and read the data from the specified file into a DataFrame
if args.transaction_file:
    try:
        df = pd.read_csv(args.transaction_file)
        print(f"Data loaded successfully from {args.transaction_file}")
        print(df.head())  # Print the first few rows of the DataFrame to verify it loaded correctly
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)
