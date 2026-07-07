from utillities.settings import Settings
from utillities.logging import Level, log_msg, log_variable, file_info

    
def is_catagory(line) -> bool:
    temp_line = line.strip().lower()
    if "$" in temp_line:
        log_msg(f"Line contains a dollar sign [NOT A CATAGORY]: {temp_line}", Level.DEBUG, file_info())
        return False
    if "everydollar" in temp_line:
        log_msg(f"Line contains 'everydollar' [NOT A CATAGORY]: {temp_line}", Level.DEBUG, file_info())
        return False
    if any(char.isdigit() for char in temp_line):
        log_msg(f"Line contains digits [NOT A CATAGORY]: {temp_line}", Level.DEBUG, file_info())
        return False
    if "favorites" in temp_line:
        log_msg(f"Line contains 'favorites' [NOT A CATAGORY]: {temp_line}", Level.DEBUG, file_info())
        return False
    log_msg(f"Line is a catagory: {temp_line}", Level.DEBUG, file_info())
    return True

def parse_catagory(line: str) -> str:
    return line.strip().split()[0].replace(" ", "-")

def make_title_friendly(string) -> str:
    return string.replace("-", " ").title()

def assign_from_account(row) -> str:
    '''This function takes a row from the budget dataframe and checks the group and category against the account map to determine which account the transfer should be made from. It returns the account name as a string.'''
    check_group = row[Settings().csv_key_map["Group"]].lower()
    check_catagory = row[Settings().csv_key_map["Category"]].lower()
    log_msg(f"Checking group [{check_group}] and category [{check_catagory}]", Level.DEBUG, file_info())
    
    # the account map is a json dictionary structured like this: account_map = {
    #        "Account": {
    #            "Group": [ 
    #               "category1",
    #               "category2" ]
    #        }
    #    }
    for account, group_catagories in Settings().ACCOUNT_MAP.items():
        log_msg(f"Account: {account} group_catagories: {group_catagories}", Level.DEBUG, file_info())
        for group, catagories in group_catagories.items():
            log_msg(f"Group: {group} catagories: {catagories}", Level.DEBUG, file_info())
            if check_group == group.lower():
                log_msg(f"!!! Group match found: {group}", Level.DEBUG, file_info())
                for catagory in catagories:
                    if check_catagory == catagory.lower():
                        log_msg(f"!!! Category match found: {catagory}", Level.DEBUG, file_info())
                        return account
    log_msg(f"NO MATCH FOUND for group: [{check_group}] and category: [{check_catagory}]", Level.ERROR, file_info())     
    return "None"

def validate_account(account_name):
    return account_name.lower() in Settings().ACCOUNTS

def audit_account_balance(budget_df, account_to_audit: str) -> float:
    if not validate_account(account_to_audit):
        log_msg(f"Invalid account specified for audit: {account_to_audit}", Level.INFO, file_info())
        return None

    budget_df[f"remaining-in-{account_to_audit}"] = budget_df.apply(lambda row: float(row[Settings().csv_key_map["Remaining"]]) if row["from-account"].lower() == account_to_audit.lower() else 0.00, axis=1)
    
    total_remaining = budget_df[f"remaining-in-{account_to_audit}"].sum() + Settings().ACCOUNT_ZERO
    log_variable(f"total_remaining_in_{account_to_audit}", total_remaining, Level.INFO, file_info())
    return total_remaining
