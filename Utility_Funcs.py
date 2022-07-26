#### Any utility should stay here. 
import requests
from datetime import datetime
import pytz

requests.packages.urllib3.disable_warnings()

def runcode():
	return """
To run python code in the chat, type:

\./run python
\`\`\`py
Your code here
\`\`\`
"""

def codeblock():
	return """
	To format your python code like this:
```py
x = 'Hello World!'
```
Type this:

\`\`\`py
Your code here
\`\`\`
"""


def get_times():
    # India
    tz_india = datetime.now(tz=pytz.timezone("Asia/Kolkata"))
    # Japan
    tz_japan = datetime.now(tz=pytz.timezone("Asia/Tokyo"))
    # America
    tz_america_ny = datetime.now(tz=pytz.timezone("America/New_York"))
    # Austria- Vienna
    tz_austria = datetime.now(tz=pytz.timezone("Europe/Vienna"))
    Times = (f"Japan (Chiaki): {tz_japan.strftime('%m/%d/%Y %I:%M %p')}"
             f"\nIndia (777advait): {tz_india.strftime('%m/%d/%Y %I:%M %p')}"
             f"\nAustria (Xarlos): {tz_austria.strftime('%m/%d/%Y %I:%M %p')}"
             f"\nAmerica (Minus): {tz_america_ny.strftime('%m/%d/%Y %I:%M %p')} ")
    return Times

    
# !embed
def Run_zeus(url):
	if "https://" in url == True:
			try:
					requests.get(url=url, timeout=2.5, verify=False)
					context = (url, "**ONLINE**")
			except requests.exceptions.ConnectionError:
					context = (url, "**OFFLINE**")

	else:
			fix_url = f"https://{url}"
			try:
					requests.get(url=fix_url, timeout=2.5, verify=False)
					context = (fix_url, "**ONLINE**")
			except requests.exceptions.ConnectionError:
					context = ("INVALID URL", "Please try again")

	return context	

# !preview
# !suggest
# !poll
# !avatar
# !owo

def help_msg():
	return """
***For-fun commands***
- !hello
- !catfact
- !dogfact
- !pugfact
- !quote
- !joke
- !8ball [question]
- !taunt
- !rolldice
- !owo [text]
- !catpic
- !dogpic [breed] (Optional)
- !pokedex [pokemon]
	
***Utility Commands***
- !codeblock
- !runcode
- !preview
- !google [question]
- !embed </br>[title]</br>[content]  
- !zeus [website]
- !fakeperson
- !poll </br>[title]</br>[options]
- !suggest [suggestion]
- !avatar/!av [member] (default=author)
- !userinfo/!whois [member] (Optional)
- !pipsearch/!pypi/!pip [package]
- !ping
- !git/!github [endpoint]
	"""


def getPypiInfo(package):
	return requests.get(f"https://pypi.org/pypi/{package}/json").json()


def getgitinfo(endpoint):
	return requests.get(f"https://api.github.com/repos/{endpoint}").json()
