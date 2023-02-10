## Info

Just a place to store shared code to be imported into the root to help instantiate the bot, and can also be used in cogs.

## Contains

### args_utils.py
Sets up an argument parser that allows passing command line arguments to the bot to configure how it's run. Currently allows you to pass --log-level, --console-log and --discord-token.

### logging_utils.py
Contains a function to abstract the configuration and instatiation of Python's base logger. This is the first thing called when anything is run. It can be configured with the passable --log-level and --console-log params, which control the level of logging and whether the logs should be streamed to the console respectively. --console-log takes a boolean which is set to True if not provided. --log-level takes an integer representing the desired level of output logs, defaulting to 10 for INFO if not provided. Read here for more details on logging - https://www.crowdstrike.com/guides/python-logging/

### mongo.py
Contains a class that implements a MongoDB client and abstracts a number of commonly used functions for ease of use.
