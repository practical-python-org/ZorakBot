
# ZorakBot
ZorakBot is the House bot of the Practical Python discord server, which was designed to be the standalone bot in the Server.
Zorak uses Py-Cord with cogged slash commands, and ties into a Mongo Database.
The bot features reaction roles, a points system, full server logging, Admin commands, spam prevention and raid protection.

Zorak is developed with features by the community. Anyone from our server can contribute.

# Deployment

Clone the bot into a folder of your choice.
```
git clone https://github.com/Xarlos89/ZorakBot
```
The bot is deployed using docker. 
Create an .env file from '.env.example'. Docker will use these env variables to spin up your instance of Zorak.
Replace the DISCORD_TOKEN env variable with your discord bot token.

## Production
```zsh
docker-compose -f dc-prod.yaml up -d
```

For testing, a separate docker-compose file is provided. 'dc-dev.yaml'
## Development / testing

You should still have the .env file from the previous steps. Make sure this contains all the relevant info.
```zsh
docker-compose -f dc-dev.yaml up -d
docker-compose -f dc-dev.yaml exec zorak python __main__.py
```
The first command will rebuild your container with the changes you made, and the second command will enter the container and start your bot.

# Contributing to Zorak

Contributing to Zorak is encouraged for everyone. Especially those who are part of our Discord community. 
We use a Prod / Development git-flow. 

To add a feature / make a bugfix, first create a new branch from the **Development** branch. This will have the most up to date changes.
Please name your branch:
- feature/whatever your feature is
- bugfix/whatever your bugfix is
- refactor/whatever your refactor is

Make all your commits on that branch, and then make a Pull Request to merge your branch back into **Development**. 

We require approvals on all PRs that go back into Dev. If your PR is linked to a Github Issue, please link the issue in the PR.

Changes will be merged into **Main** when there are changes to merge.

 ### Git-Flow chart
The chart below demonstrates one feature, and one bugfix. 
Main and Development already exist. You would want to make a new branch for whatever you're going to do.



![Untitled Diagram.drawio.png](..%2F..%2FDesktop%2FUntitled%20Diagram.drawio.png)