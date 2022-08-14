# ZorakBot

ZorakBot is the House bot of the Practical Python discord server. Zorak is developed with features by the community. Anyone from our server can contribute. 


## User Commands
#### For-fun commands
- z.hello
- z.catfact
- z.dogfact
- z.pugfact
- z.quote
- z.joke
- z.8ball [question]
- z.taunt
- z.rolldice
- z.catpic
- z.dogpic [breed] (Optional)
- z.pokedex [pokemon]
#### Utility Commands
- z.google [question]
- z.embed [title] [ content ]  
- z.zeus [website]
- z.fakeperson
- z.userinfo/z.whois
- z.avatar/z.av
- z.ping
- z.pipsearch/z.pypi/z.pip [package]
- z.git/z.github [endpoint]
#### Admin Commands
- z.echo [message]
- z.rules [title] [rules]

## Deployment

Optional arguments: 

| Parameter |   Long Parameter   |                                     Default                                     | Description                                               |
| :-------- | :----------------: | :-----------------------------------------------------------------------------: | :-------------------------------------------------------- |
| -h        |       --help       |                                                                                 | Show help message and exit program                        |
| -scf      |  --s3-config-file  |                                      None                                       | S3 or Local location of the S3 config file                |
| -ecf      |  --es-config-file  |                                      None                                       | S3 or Local location of the ElasticSearch config          |
| -cb       | --config-bucket-s3 |                            vtk-city-service-configs                             | S3 bucket where all config files are stored               |
| -tc       |   --thread-count   |                                        8                                        | Number of threads to use for processing individual frames |
| -ll       |    --log-level     | INFO [(Enum 20)](https://docs.python.org/3/library/logging.html#logging-levels) | Logger level                                              |

Optional flags:

| True Flag     |    False Flag    | Default | Description                 |
| :------------ | :--------------: | :-----: | :-------------------------- |
| --console-log | --no-console-log |  True   | Flag for logging to console |
| --local       |    --no-local    |  True   | Are the config files local  |