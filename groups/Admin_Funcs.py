import os

def send_echo(message):
	#check if user has provided a message to display
	if message:
		return message
  # otherwise let user know they need to add a message
	return "Please enter a message to echo."

# TODO: Recreate the daily challenges, and bring this back to life
# def DailyChallenge():
#   dayPath = '/home/runner/Zorak/2_Challenges/day.txt'
#   path = '/home/runner/Zorak/2_Challenges/'
  
#   with open(dayPath) as ChallengeOfTheDay:
#     searchterm = 'Python daily challenge - Day {}'.format(ChallengeOfTheDay.read())
#     openFolder = os.listdir((path + searchterm))
#     if 'Question.txt' in openFolder:
#         filepath = (path + searchterm) + '/' + 'Question.txt'
#         with open(filepath) as file:
#             challenge = file.read()
#             return challenge
#     else:
#         print('Shit, no challenge today... someone tell Xarlos that I have a bug.')

# def increaseDay():
#   dayPath = '/home/runner/Zorak/2_Challenges/day.txt'
#   with open(dayPath, 'r+') as file:
#       day = str(int(file.read()) + 1)
#       file.seek(0)
#       file.write(day)
