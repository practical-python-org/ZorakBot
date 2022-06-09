from bs4 import BeautifulSoup
from time import sleep
from os import system
import requests
import random
import json
import os
import time 


def taunt():
	r = requests.get('https://fungenerators.com/random/insult/shakespeare/')
	soup = BeautifulSoup(r.content, "html.parser")
	taunt = soup.find('h2')
	return taunt.text
	
def pugFact():
	r = requests.get('https://fungenerators.com/random/facts/dogs/pug')
	soup = BeautifulSoup(r.content, "html.parser")
	pugFact = soup.find('h2')
	return pugFact.text[:-15]

def dogfact():
  return(json.loads(requests.get('https://dog-api.kinduff.com/api/facts').text)['facts'][0])

def catfact():
  return(json.loads(requests.get('https://catfact.ninja/fact').text)['fact'])

def catpic():
	r = requests.get('http://aws.random.cat/meow').text
	return(r[9:-2])

def joke():
  return(json.loads(requests.get('https://geek-jokes.sameerkumar.website/api?format=json').text)['joke'])
  
def quote():
	quote = json.loads(requests.get('https://zenquotes.io/api/random').text)[0]
	return (quote['q'] + "\n- " + quote['a'])

def DailyChallenge():
  dayPath = '/home/runner/Zorak/2_Challenges/day.txt'
  path = '/home/runner/Zorak/2_Challenges/'
  
  with open(dayPath) as ChallengeOfTheDay:
    searchterm = 'Python daily challenge - Day {}'.format(ChallengeOfTheDay.read())
    openFolder = os.listdir((path + searchterm))
    if 'Question.txt' in openFolder:
        filepath = (path + searchterm) + '/' + 'Question.txt'
        with open(filepath) as file:
            challenge = file.read()
            return challenge
    else:
        print('Shit, no challenge today... someone tell Xarlos that I have a bug.')

def increaseDay():
  dayPath = '/home/runner/Zorak/2_Challenges/day.txt'
  with open(dayPath, 'r+') as file:
      day = str(int(file.read()) + 1)
      file.seek(0)
      file.write(day)

def magik():
    MagikList = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs points to yes.", "Reply hazy, try again.", "Ask again later.", "Better not to tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good", "Very doubtful.", "Be more polite.", "How would i know", "100%", "Think harder", "Sure""In what world will that ever happen", "As i see it no.", "No doubt about it", "Focus", "Unfortunately yes", "Unfortunately no,", "Signs point to no"]
    return random.choice(MagikList)
	

def fakePerson():
	person = json.loads(requests.get('https://randomuser.me/api/').text)['results']
	name = 'Name: {} {} {}'.format(person[0]['name']['title'],person[0]['name']['first'],person[0]['name']['last'])
	hometown = 'Hometown: {}, {}'.format(person[0]['location']['city'],person[0]['location']['country'])
	age = 'Age: {} Years old'.format(person[0]['dob']['age'])
	generateUser = 'You have requested a fake person:\n\n' + name + '\n'+ hometown + '\n' + age
	return generateUser

def dice():
	roll = ['1','2','3','4','5','6']
	result = random.choice(roll)
	return result

def check_site(url):
	if "https://" in url == True:
			try:
					requests.get(url=url, timeout=2.5, verify=False)
					context = (url, "**ONLINE**")
			except requests.exceptions.ConnectionError:  # if the site is not online, the program will raise an exception.
					context = (url, "**OFFLINE**")
	#main function to check the status of websites.
	else:
			fix_url = f"https://{url}"
			try:
					requests.get(url=fix_url, timeout=2.5, verify=False)
					context = (fix_url, "**ONLINE**")
			except requests.exceptions.ConnectionError:  # if the site is not online, the program will raise an exception.
					context = ("INVALID URL", "Please try again")

	return context

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
***Utility Commands***
- !google [question]
- !embed </br>[title]</br>[content]  
- !zeus [website]
- !fakeperson
- !poll </br>[title]</br>[options]
- !suggest [suggestion]
- avatar [member] (default=author)
***Admin Commands***
- !echo [message]
- !dailychallenge
- !rules </br>[title]</br>[rules]
	"""