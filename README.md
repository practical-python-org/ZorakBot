
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

### Locally
The easiest way to get started is to run Zorak locally and in our test server (Contact a repo admin for an invite!). To do this, clone the repo, cd into the root and hit
```zsh
pip install .
zorak -dt <DISCORD_TOKEN_HERE> -ssp Resources/ServerConfig/Zorak-Dev -dd True -cl True
```

-ssp: Variable that sets the location to the server settings to use.
-dd: Flag that allows you to drop the database.
-cl: Flag that enables streaming logs to console.

### Docker Setup
/setting up with Docker lets you use and develop some of Zorak's more complex features as it gives you access to the mongo container that's spun up alongside Zorak on server.

You should still have the .env file from the previous steps. Make sure this contains all the relevant info.
```zsh
docker-compose -f docker-compose.yaml up -d
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

## Version Bumping through PR titles
Our repository uses an automated versioning system that relies on the naming convention of the pull request titles. When you merge a pull request into the dev branch, the version number of the project is automatically bumped and a new tag is created, based on the prefix in your PR title.

The version number follows the MAJOR.MINOR.FIX format, where:

MAJOR version increments indicate significant changes or enhancements in the project, often including breaking changes. MINOR version increments indicate backwards-compatible new features or enhancements. FIX version increments indicate backwards-compatible bug fixes or minor changes. To specify the type of changes you have made in your pull request, prefix your PR title with one of the following:

major: - to increment the MAJOR version (e.g., from 1.0.0 to 2.0.0). minor: - to increment the MINOR version (e.g., from 0.1.0 to 0.2.0). fix: - to increment the FIX version (e.g., from 0.0.1 to 0.0.2). For example, if you have made a minor change, your PR title could be: minor: Add new feature XYZ.

If your PR title does not include any of the specified prefixes, the GitHub Action will not increment the version or create a new tag. This can be useful for non-functional changes like updates to documentation or code refactoring that don't require a version bump.

When your PR is merged into main, the GitHub Action will increment the version according to the prefix in the PR title and create a new tag.

Please ensure you follow this convention to maintain a well-structured and meaningful version history for our project.

 ### Git-Flow chart
The chart below demonstrates one feature, and one bugfix. 
Main and Development already exist. You would want to make a new branch for whatever you're going to do.



![Untitled Diagram.drawio.png](..%2F..%2FDesktop%2FUntitled%20Diagram.drawio.png)