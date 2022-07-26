import os
from datetime import datetime
import pytz

def DailyChallenge():
  dayPath = '/home/runner/Zorak/2_Challenges/day.txt'
  path = '/home/runner/Zorak/2_Challenges/'
  
  with open(dayPath) as ChallengeOfTheDay:
    searchterm = 'Python daily challenge - Day {}'.format(ChallengeOfTheDay.read())
    openFolder = os.listdir((path + searchterm))
    if 'Question.txt' in openFolder:
        filepath = (path + searchterm) + '/' + 'Question.txt'
        with open(filepath) as file:
            challenge = file.read()
            return challenge
    else:
        print('Shit, no challenge today... someone tell Xarlos that I have a bug.')

def increaseDay():
  dayPath = '/home/runner/Zorak/2_Challenges/day.txt'
  with open(dayPath, 'r+') as file:
      day = str(int(file.read()) + 1)
      file.seek(0)
      file.write(day)


def get_times():
    # India
    tz_india = datetime.now(tz=pytz.FixedOffset(330))
    # Japan
    tz_japan = datetime.now(tz=pytz.timezone("Asia/Tokyo"))
    # America
    tz_america_ny = datetime.now(tz=pytz.timezone("America/New_York"))
    # Austria- Vienna
    tz_austria = datetime.now(tz=pytz.timezone("Europe/Vienna"))
    Times = (f"Japan: {tz_japan.strftime('%m/%d/%Y %I:%M %p')}"
             f"\nIndia: {tz_india.strftime('%m/%d/%Y %H:%M %p')}"
             f"\nAustria: {tz_austria.strftime('%m/%d/%Y %I:%M %p')}"
             f"\nAmerica: {tz_america_ny.strftime('%m/%d/%Y %I:%M %p')} ")
    return Times

