
# ZorakBot
ZorakBot is the House bot of the Practical Python discord server. Zorak is developed with features by the community. Anyone from our server can contribute.

Zorak uses PyCord and slash commands.
Currently, the bot is "fun" and utility heavy, Admin features are planned.

# Commands and Features
### Help
- [X] - /help
	- [X] - /ping
	- [X] - /commands
	- [X] - /run_code
	- [X] - /code_blocks

### For-fun commands
- [X] - /hello
- [X] - /taunt
- [X] - /catfact
- [X] - /dogfact
- [X] - /pugfact
- [X] - /catpic
- [X] - /dogpic arg:[breed]
- [X] - /joke
- [X] - /quote
- [X] - /fakeperson
- [X] - /google arg:[question]
- [X] - /pokedex arg:[pokemon]
- [X] - /rolldice
- [X] - /8ball arg:[question]
- [X] - /drawme arg:[text] arg:[seed]
- [X] - /imbored

### Utility Commands
- [X] - /run \`\`\`py print('hello world')\`\`\`
- [X] - /pip_search arg:[package]
- [X] - /github_search arg:[endpoint]
- [X] - /devtimes
- [X] - /zeus arg:[website]
- [ ] - /latex arg:[formula]
- [ ] - /avatar arg:[user]
- [ ] - /poll arg:[title] arg:[option1] arg:[option2] arg:[option3]...
- [ ] - /whois arg:[user]

### Admin-Only Commands
- [X] - /test
- [X] - /embed arg:[title] arg:[content]
- [X] - /suggest arg:[suggestion]

### Cool Tricks
- [X] - When a link to a discord message is sent in a channel, Zorak will preview that message.
- [X] - Zorak utilizes Piston API to run code directly in the server.
- [X] - Verifies new users with a verification button.


# To-do
| Bugs |
|--|
| Fix /avatar (Message deleted, but nothing returned.) |
| Fix /whois (Message deleted, but nothing returned.) |
| Fix /userinfo//whois (Message deleted, but nothing returned.) |



### Features
- [X] - Welcome message for new members.
- [X] - Welcome PM for new members.
- [X] - Role management for new members.
- [X] - Run code within the server.
- [ ] - Word blacklist functionality
- [X] - Suspicious link detection and removal
- [ ] - Muting spam messages across multiple channels
- [ ] - Server lockdown feature




# Deployment
Clone the bot into a folder of your choice.

```
git clone https://github.com/Xarlos89/ZorakBot
```
## Docker
The bot is deployed using docker. Replace the YOUR_BOT_TOKEN with your discord bot token.

### Development Workflow
```zsh
docker-compose -f dc-dev.yaml up -d
docker-compose -f dc-dev.yaml exec zorak python __main__.py
docker-compose -f dc-dev.yaml down --rmi local
```

<p class="callout warning"> Note: If you make changes to the .env variables you will need to bring down the docker stack and back up</p>

### Production Deployment

```zsh
docker-compose -f dc-prod.yaml up -d
```

## ENV example:

```ini
# General Settings
DISCORD_TOKEN=Some_Junk_Here #secret token found here https://discord.com/developers/applications
TAG=0.2
DEV_SETTINGS=TRUE

# Logging
LOGGING_LEVEL=20 #DEBUG 10
STREAM_LOGS=FALSE
```
