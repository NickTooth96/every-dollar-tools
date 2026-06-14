import csv
import wget
from pypdf import PdfReader
from utillities.utillities import Level, is_catagory, log_msg, parse_catagory



def pdf_to_text(pdf_path, txt_path):
    # Load the PDF file
    reader = PdfReader(pdf_path)
    
    # Extract text from all pages
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    # Write to a text file
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)

def clean_text_file(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = []
    current_category = None
    for line in lines:
        # Remove leading/trailing whitespace and skip empty lines
        cleaned_line = line.strip()
        if is_catagory(cleaned_line):
            if parse_catagory(cleaned_line) != current_category:
                current_category = parse_catagory(cleaned_line)
            continue
        if cleaned_line.startswith("Page "):
            continue  # Skip page number lines
        if cleaned_line.startswith("$"):
            continue  # Skip lines that start with a dollar sign (assuming they are totals or headers)
        if ("EveryDollar") in cleaned_line:
            continue  # Skip lines that contain "EveryDollar"
        if ("Budget") in cleaned_line:
            continue  # Skip lines that contain "Budget"
        if ("$") not in cleaned_line:
            continue  # Skip lines that do not contain a dollar sign
        for x in cleaned_line.split(" "):
            if x.startswith(","):
                cleaned_line = cleaned_line.replace(" ,", "")  # Remove commas from the line
        cleaned_line = f"{current_category} {cleaned_line}"  # Prepend the current category to the line
        # write back the cleaned line to the the list of cleaned lines if it is not empty
        if cleaned_line:
            cleaned_lines.append(cleaned_line)

    # Write the cleaned lines back to the file
    with open(f"{txt_path}.new", "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines))

def make_budget_file_csv(txt_path, csv_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    data = []
    for line in lines:
        parts = line.split()
        if "-" in parts:
            parts = [x for x in parts if x != '-']
        group = parts.pop(0) # Assuming the group is the first part
        amount = parts[-2]  # Assuming the amount is the second to last part
        remaining = parts[-1]  # Assuming the remaining is the last part
        if len(parts) <= 5:
            category = " ".join(parts[:-2]).replace(" ", "-").strip()  # Remove any dollar signs and extra whitespace
        else:
            for x in parts:
                if "due" in x.lower():
                    index = parts.index(x)
                    # replacae the part with due with the same thing minus "due" and remove the next two parts after it
                    parts[index] = parts[index].replace("Due", "").strip()
                    del parts[index+1:index+3]
            category = " ".join(parts[:-2]).replace(" ", "-").strip()

        if ":" in category:
            category = category.replace(":", "").strip()
        if not amount.startswith("$"):
            temp_amount = amount.split("$")
            amount = f"${temp_amount[1]}"
            category += f"-{temp_amount[0].strip()}"
        data.append((group, category, amount, remaining))

    # Write the data to a CSV file
    with open(csv_path, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Group", "Category", "Amount", "Remaining"])  # Write header
        for row in data:
            writer.writerow(row)  # Write each row


def grab_pdf_from_url(url, output_path):
    try:
        wget.download(url, output_path)
        log_msg(f"PDF downloaded successfully from {url} to {output_path}", Level.INFO)
    except Exception as e:
        log_msg(f"Error downloading PDF: {e}", Level.ERROR)