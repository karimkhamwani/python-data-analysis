import pandas as pd
import re
import numpy as np
from email_validator import validate_email
import ipaddress


# look if value is missing?
def isMissingValue(value):
    if(type(value) == float):
        return 0      
    else:
        return 1

# valided ip address
def validateIpAddress(ip):
    if(isMissingValue(ip)): return 0
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

# check if value is mising then value will be nan
def getNameScore(name):
    if(type(name) == float):
        return 0
    else:
        return 1

pd.options.display.max_columns = None
pd.options.display.width=None
pd.options.display.max_rows = None

#reading csv file
accounts_csv = pd.read_csv('./account_log_without_labels.csv')


accounts_csv = accounts_csv.head(2)

print(validateIpAddress('170.45.171.112'))

#steps
# 1 - convert categorical data into numeric
# 2 - add new column in df for each categorical data
# 3 - sum the score to determine fraud or not.
# 4 - assign each some a campagine

# Rules ( final values for score would be between 1 or 0 )    
# email score : valid or fake email address
# name score : if name is missing
# geography score : if location not exists and fake ip address


#loop over csv
for index in accounts_csv.index:
    # print(index)
    email = accounts_csv['email'][index]
    name = accounts_csv['name'][index]
    accounts_csv.loc[index, 'emailScore'] = validateEmail(email)
    accounts_csv.loc[index, 'nameScore'] = getNameScore(name)


print(accounts_csv)
# print(accounts_csv["email"].value_counts())