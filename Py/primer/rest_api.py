import config

'''Define config variables for API. B19013_001E is the Census label for Median Household Income (estimate).'''
STATE = "state:36"
TRACT = "tract:*"
KEY = config.apptoken
VAR = "B19013_001E"
URL ="https://api.census.gov/data/2019/acs/acs5?"

'''Census API call using the Requests library that gets the reponse and does some very basic error catching'''
try:
    response = requests.get(URL, params = {"get" : VAR, "for" : TRACT, "in" : STATE, "key" : KEY})
    response.raise_for_status() #raise exception
    df = pd.DataFrame.from_dict(response.json())
except requests.exceptions.HTTPError as err_http: #catches Http errors
    print(err_http)
except requests.exceptions.TooManyRedirects as err_redir:
    print(err_redir)

'''Minimal reformatting using Pandas to drop unnecesary columns, change datatypes and assign NaN to non-existent values'''
header = df.iloc[0]
df = df[1:]
df.columns = header
df = df.drop("state", axis=1)
df["B19013_001E"] = pd.to_numeric(df["B19013_001E"])
df.loc[df["B19013_001E"] < 0, "B19013_001E"] = np.NaN

'''Insights magic return function. Make sure you place this command in a separate cell'''
%insights_return(df)