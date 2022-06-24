#### Any non-utility "Fun functions" should stay here. 
from io import BytesIO
from bs4 import BeautifulSoup
import requests
import random
import json

requests.packages.urllib3.disable_warnings()

def hello():
	return "Don't talk to me, I am being developed!"

def taunt():
	r = requests.get('https://fungenerators.com/random/insult/shakespeare/')
	soup = BeautifulSoup(r.content, "html.parser")
	taunt = soup.find('h2')
	return taunt.text

def catfact():
  return(json.loads(requests.get('https://catfact.ninja/fact').text)['fact'])

def dogfact():
  return(json.loads(requests.get('https://dog-api.kinduff.com/api/facts').text)['facts'][0])
					
def pugFact():
	r = requests.get('https://fungenerators.com/random/facts/dogs/pug')
	soup = BeautifulSoup(r.content, "html.parser")
	pugFact = soup.find('h2')
	return pugFact.text[:-15]

def catpic():
	return BytesIO(requests.get("https://cataas.com/cat").content)


def joke():
  return(json.loads(requests.get('https://geek-jokes.sameerkumar.website/api?format=json').text)['joke'])
  
def quote():
	quote = json.loads(requests.get('https://zenquotes.io/api/random').text)[0]
	return (quote['q'] + "\n- " + quote['a'])

def eightball():
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

def dogpic(breed):
	if breed==" ":
		return requests.get("https://dog.ceo/api/breeds/image/random").json()["message"]
	
	return requests.get(f"https://dog.ceo/api/breed/{breed}/images/random").json()["message"]

# print(dogpic())