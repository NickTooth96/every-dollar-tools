from utillities.settings import Settings
from utillities.logging import Level, log_msg

    
def is_catagory(line) -> bool:
    temp_line = line.strip().lower()
    if "$" in temp_line:
        return False
    if "everydollar" in temp_line:
        return False
    if any(char.isdigit() for char in temp_line):
        return False
    if "favorites" in temp_line:
        return False
    return True

def parse_catagory(line: str) -> str:
    return line.strip().split()[0].replace(" ", "-")

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
    for account, group_catagories in Settings().ACCOUNT_MAP.items():
        log_msg(f"Account: {account} group_catagories: {group_catagories}", Level.DEBUG)
        for group, catagories in group_catagories.items():
            log_msg(f"Group: {group} catagories: {catagories}", Level.DEBUG)
            if check_group == group.lower():
                log_msg(f"!!! Group match found: {group}", Level.DEBUG)
                for catagory in catagories:
                    if check_catagory == catagory.lower():
                        log_msg(f"!!! Category match found: {catagory}", Level.DEBUG)
                        return account        
    return "None"

def validate_account(account_name):
    return account_name.lower() in Settings().ACCOUNTS

def audit_account_balance(budget_df, account_to_audit: str) -> float:
    if not validate_account(account_to_audit):
        log_msg(f"Invalid account specified for audit: {account_to_audit}", Level.INFO)
        return None

    budget_df[f"remaining-in-{account_to_audit}"] = budget_df.apply(lambda row: float(row["Remaining"].replace("$", "").replace(",", "")) if row["from-account"].lower() == account_to_audit.lower() else 0.00, axis=1)
    
    total_remaining = budget_df[f"remaining-in-{account_to_audit}"].sum() + Settings().ACCOUNT_ZERO
    return total_remaining
