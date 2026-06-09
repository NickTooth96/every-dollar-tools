import json


DEBUG = False
ACCOUNT_ZERO = float(1000.00)

ACCOUNT_MAP = json.load(open("utillities/account-map.json", "r"))
ACCOUNTS = ACCOUNT_MAP.keys()

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
    for account, group_catagories in ACCOUNT_MAP.items():
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

def validate_account(account_name):
    return account_name.lower() in ACCOUNTS

def audit_account_balance(budget_df, account_to_audit: str) -> float:
    if not validate_account(account_to_audit):
        print(f"Invalid account specified for audit: {account_to_audit}")
        return None

    budget_df[f"remaining-in-{account_to_audit}"] = budget_df.apply(lambda row: float(row["Remaining"].replace("$", "").replace(",", "")) if row["from-account"].lower() == account_to_audit.lower() else 0.00, axis=1)
    
    total_remaining = budget_df[f"remaining-in-{account_to_audit}"].sum() + ACCOUNT_ZERO
    return total_remaining
