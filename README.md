# ZorakBot

ZorakBot is the House bot of the Practical Python discord server. Zorak is developed with features by the community. Anyone from our server can contribute. 


# User Commands
### For-fun commands
- [X] - z.hello
- [X] - z.catfact
- [X] - z.dogfact
- [X] - z.pugfact
- [X] - z.quote
- [X] - z.joke
- [X] - z.8ball [question]
- [X] - z.taunt
- [X] - z.rolldice
- [X] - z.catpic
- [X] - z.dogpic [breed] (Optional)
- [X] - z.pokedex [pokemon]
- [X] - z.drawme "text" (Required string) [seed] (Optional int)

### Utility Commands
- [X] - z.codeblock
- [X] - z.runcode
- [X] - z.google [question]
- [X] - z.embed </br>[title]</br>[content]
- [X] - z.zeus [website]
- [X] - z.fakeperson
- [X] - z.poll </br>[title]</br>[options]
- [X] - z.suggest [suggestion]
- [X] - z.avatar/z.av [member] (default=author)
- [X] - z.userinfo/z.whois [member] (Optional)
- [X] - z.pipsearch/z.pypi/z.pip [package]
- [X] - z.ping
- [X] - z.git/z.github [endpoint]

### Cool Tricks
- [X] - When a link to a discord message is sent in a channel, Zorak will preview that message.

### Admin Commands
- [X] - z.echo [message]
- [X] - z.rules [title] [rules]

### To-do
- [ ] - Fix z.pokedex command. (Just does not work.)
- [ ] - Fix z.poll (Only sets one emoji.)
- [ ] - Fix z.avatar (Message deleted, but nothing returned.)
- [ ] - Fix z.userinfo/z.whois (Message deleted, but nothing returned.)
- [ ] - Fix z.git/z.github (Does not find repos, or does not respond.)
- [ ] - Fix z.times (command is unrecognized)




## Deployment

Run 'pip install .' in the root directory to pull all dependencies and create a build of zorak_module. Build is then runnable via a call to  zorak_bot/__main__.py script.

If you're developing on the project you won't want to rebuild the module each time you make a change, so you can do this once to set up your enviroment before running 'pip uninstall zorak_bot' and then continuing to run zorak_bot/__main__.py. Alternitevely if using VSCode install the Jupyter extension and you can add '#%%' at the top of __main__.py (or anywhere for that matter) to run/debug the below code as a Jupyter cell.

Optional arguments: 

| Parameter |   Long Parameter   |                                     Default                                     | Description                                               |
| :-------- | :----------------: | :-----------------------------------------------------------------------------: | :-------------------------------------------------------- |
| -dt       |    --discord_token |                                      None                                       | Token for the connection to discord. If not icluded TOKEN env variable is used. |
| -lf       |    --log_file      |                                      None                                       | .log file to output logs to. No output if left as default |
| -ef       |    --err_file      |                                      None                                       | .log file to output errs to. No output if left as default |
| -ll       |    --log-level     | INFO [(Enum 20)](https://docs.python.org/3/library/logging.html#logging-levels) | Logger level                                              |

Optional flags:

| True Flag     |    False Flag    | Default | Description                 |
| :------------ | :--------------: | :-----: | :-------------------------- |
| --console-log | --no-console-log |  True   | Flag for logging to console |
