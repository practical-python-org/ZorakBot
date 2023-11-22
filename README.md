
# ZorakBot
ZorakBot is the House bot of the Practical Python discord server. 

Its purpose is to moderate, log, and provide necessary features that the community deems worthy. Anyone from our community is welcome to join us in developing the bot. 
Zorak uses Py-Cord with cogged slash commands, and ties into a Mongo Database.

The bot features:
- Reaction roles
- A points system
- Music functions
- Admin commands
- Full server logging
- Spam prevention 
- Raid protection.

---
# Deployment / Running Zorak
Clone the bot into a folder of your choice.
```
git clone https://github.com/Xarlos89/ZorakBot
```
The bot is deployed using docker. 
Create an .env file from '.env.example'. Docker will use these env variables to spin up your instance of Zorak.
Replace the DISCORD_TOKEN env variable with your discord bot token.

### Development / testing
The easiest way to get started is to run Zorak locally and in our test server (Contact a repo admin for an invite!). 
- -ssp: Variable that sets the location to the server settings to use.
- -dd: Flag that allows you to drop the database.
- -cl: Flag that enables streaming logs to console.

```bash
docker-compose up -d
```
And then after making a change, rebuild only zorak.
```bash
docker build -t zorak .
docker run --env-file ./.env zorak -dd True -dt <DISCORD_TOKEN_HERE>
```


### Production
All environment settings are found in your .env file.
1. Update the .env file to use 'prod' as the ENVIRONMENT
2. Update your .env file to point the SETTINGS variable to Resources/ServerConfig/PracticalPython
3. Run the command:
```bash
docker-compose up -d
```

---
# Get Involved with development

Contributing to Zorak is encouraged for everyone. Especially those who are part of our Discord community. 
We use a Prod / Development git-flow. 
### Branches
To add a feature / make a bugfix, first create a new branch from the **Development** branch. This will have the most up to date changes.
Please name your branch in the following format:
- feature/whatever your feature is 
- bugfix/whatever your bugfix is 
- refactor/whatever your refactor is

### Pull Requests
Make all your commits on that branch, and then make a Pull Request to merge your branch back into **Development**.
Please name your pull request in the following format:
- major: Title of your major changes
- minor: Title of your minor changes
- fix: Title of your bugfixes

We require approvals on all PRs that go back into Dev. If your PR is linked to a Github Issue, please link the issue in the PR.

Changes will be merged into **Main** when necessary


### Git-Flow chart
The chart below demonstrates one feature, and one bugfix. 
Main and Development already exist. You would want to make a new branch for whatever you're going to do.



![git-flow](https://github.com/practical-python-org/ZorakBot/assets/33434582/9d04d6a1-305f-48d9-8cee-be3ad08e099f)



### Version Bumping through PR titles
Our repository uses an automated versioning system that relies on the naming convention of the pull request titles. When you merge a pull request into the dev branch, the version number of the project is automatically bumped and a new tag is created, based on the prefix in your PR title.

The version number follows the MAJOR.MINOR.FIX format, where:

MAJOR version increments indicate significant changes or enhancements in the project, often including breaking changes. MINOR version increments indicate backwards-compatible new features or enhancements. FIX version increments indicate backwards-compatible bug fixes or minor changes. To specify the type of changes you have made in your pull request, prefix your PR title with one of the following:

major: - to increment the MAJOR version (e.g., from 1.0.0 to 2.0.0). minor: - to increment the MINOR version (e.g., from 0.1.0 to 0.2.0). fix: - to increment the FIX version (e.g., from 0.0.1 to 0.0.2). For example, if you have made a minor change, your PR title could be: minor: Add new feature XYZ.

If your PR title does not include any of the specified prefixes, the GitHub Action will not increment the version or create a new tag. This can be useful for non-functional changes like updates to documentation or code refactoring that don't require a version bump.

When your PR is merged into main, the GitHub Action will increment the version according to the prefix in the PR title and create a new tag.

Please ensure you follow this convention to maintain a well-structured and meaningful version history for our project.

