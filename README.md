# ZorakBot

ZorakBot is the House bot of the Practical Python discord server. Zorak is developed with features by the community. Anyone from our server can contribute. 


# User Commands
### For-fun commands
- [X] - /hello
- [X] - /catfact
- [X] - /dogfact
- [X] - /pugfact
- [X] - /quote
- [X] - /joke
- [X] - /8ball arg:[question]
- [X] - /taunt
- [X] - /rolldice
- [X] - /catpic
- [X] - /dogpic arg:[breed]
- [X] - /pokedex arg:[pokemon]
- [X] - /drawme arg:[text] arg:[seed]

### Utility Commands
- [X] - /codeblock
- [X] - /runcode
- [X] - /google arg:[question]
- [X] - /embed arg:[title] arg:[content]
- [X] - /zeus arg:[website]
- [X] - /fakeperson
- [X] - /suggest arg:[suggestion]
- [X] - /pip_search arg:[package]
- [X] - /ping
- [X] - /github_search arg:[endpoint]
- [ ] - /latex arg:[formula]
- [ ] - /avatar arg:[user]
- [ ] - /poll arg:[title] arg:[option1] arg:[option2] arg:[option3]...
- [ ] - /whois arg:[user]



### Cool Tricks
- [X] - When a link to a discord message is sent in a channel, Zorak will preview that message.

### Admin Commands
- [X] - /echo [message]
- [X] - /rules [title] [rules]

### To-do
- [ ] - Fix /pokedex command. (Just does not work.)
- [ ] - Fix /poll (Only sets one emoji.)
- [ ] - Fix /avatar (Message deleted, but nothing returned.)
- [ ] - Fix /userinfo//whois (Message deleted, but nothing returned.)
- [ ] - Fix /git//github (Does not find repos, or does not respond.)
- [ ] - Fix /times (command is unrecognized)




## Deployment
The bot is deployed using docker. Replace the YOUR_BOT_TOKEN with your discord bot token. 

cd /zorak_bot
docker build -t zorak_bot .
docker run -d zorak_bot YOUR_BOT_TOKEN
docker rename CONTAINER Zorak
docker start Zorak
docker stop Zorak