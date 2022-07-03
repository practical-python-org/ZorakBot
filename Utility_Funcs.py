#### Any utility should stay here. 
import requests

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
	"""


def getPypiInfo(package):
	return requests.get(f"https://pypi.org/pypi/{package}/json").json()