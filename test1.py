import pandas as pd
import re
import numpy as np
from email_validator import validate_email
import ipaddress
import re


# look if value is missing?
def valueExists(value):
    if type(value) == float:
        return 0
    else:
        return 1


# valided ip address
def validateIpAddress(ip):
    try:
        ipaddress.ip_address(ip)
        return 1
    except:
        return 0


# look if email is valid of not
def validateEmail(email):
    try:
        # Validating the email
        validate_email(email)
        return 1
    except:
        return 0


pd.options.display.max_columns = None
pd.options.display.width = None
pd.options.display.max_rows = None

# reading csv file
accounts_csv = pd.read_csv("./account_log_without_labels.csv")


# accounts_csv = accounts_csv.head(10)

# steps
# 1 - convert categorical data into numeric
# 2 - add new column in df for each categorical data
# 3 - sum the score and divide bby total number of senecrios considered
# 4 - assign each row with campagine and macilious value

# Rules ( final values for score would be between 1 or 0 )
# email score : valid or fake email address
# geography score : if location not exists and fake ip address
# duplication score : if more than one account is created with same email and same account name

# loop over csv
for index in accounts_csv.index:
    print(index)
    email = accounts_csv["email"][index]
    name = accounts_csv["name"][index]
    account = accounts_csv["account"][index]
    location = accounts_csv["location"][index]
    ipAddress = accounts_csv["ip_address"][index]
    accounts_csv.loc[index, "city"] = (
        location.split(",")[0] if valueExists(location) else ""
    )
    accounts_csv.loc[index, "emailScore"] = valueExists(email) * validateEmail(email)
    accounts_csv.loc[index, "systemAuthenticityScore"] = validateIpAddress(ipAddress)
    accounts_csv.loc[index, "botScore"] = (
        0 if (account == name and str(re.search(account, email)) != "None") else 1
    )
    # look if more than one account is created with same email and account name,
    # bcz it doesnt make any sense 1 person creating two accounts?
    accounts_csv.loc[index, "duplicationScore"] = (
        0
        if (
            (accounts_csv["email"] == email).sum() > 1
            and (accounts_csv["account"] == account).sum() > 1
        )
        else 1
    )
    percentage = (
        (
            accounts_csv.loc[index, "emailScore"]
            + accounts_csv.loc[index, "systemAuthenticityScore"]
            + accounts_csv.loc[index, "duplicationScore"]
            + accounts_csv.loc[index, "botScore"]
        )
        / 4
    ) * 100
    accounts_csv.loc[index, "isRealUser"] = round(percentage, 2)
    realityScore = accounts_csv.loc[index, "isRealUser"]
    accounts_csv.loc[index, "malicious_account"] = False if percentage > 80 else True
    accounts_csv.loc[index, "campaign"] = (
        "legit"
        if realityScore > 80
        else "warriors"
        if realityScore >= 50 and realityScore <= 80
        else "fighters"
    )

accounts_csv.to_csv("test.csv")
