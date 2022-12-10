import requests
import json
from  datetime import date, datetime, timedelta
import pytz
 
DISCORD_EMOJI_WRONG = ":no_entry_sign:"
DISCORD_EMOJI_RIGHT = ":white_check_mark:"

FIRST_HOUR_CHAR_INDEX = 11
LAST_HOUR_CHAR_INDEX = -7
LAST_DATE_CHAR_INDEX = 10

TIMEZONE = 'America/Sao_Paulo'
datetime.utcnow().replace(tzinfo=pytz.timezone(TIMEZONE))

today = date.today()
timezoneDiff = -3

# put here your friends github usernames and their discord id's

targetsInfo = [
  {"username": "Gabriel-S-O", "discordId": "173421126901432320"},
  {"username": "Gakjvc", "discordId": "291344422975832064"},
  {"username": "GUGALU", "discordId": "537656953137004555"},
  {"username": "Ruan-F-M", "discordId": "961780118479573032"}
  ]

usersAsObject = []

messages = []

class User(object):
  def __init__ (self, name, commited, discordId):
    self.name = name
    self.commited = "DID COMMIT" if commited else "DID NOT COMMIT"
    self.discordId = discordId


def get_user_github_events(user):
  userEvents = requests.get("https://api.github.com/users/{user}/events".format(user = user))
  return json.loads(userEvents.text)

def build_users(userName, commited, discordId):
  user = User(userName, commited, discordId)
  usersAsObject.append(user)

def save_users_activities():
  for userObject in usersAsObject:
    emoji = DISCORD_EMOJI_RIGHT if userObject.commited == "DID COMMIT" else DISCORD_EMOJI_WRONG
    message = ("{} <@{}> **{}** {}".format(emoji,userObject.discordId, userObject.commited, emoji))
    messages.append(message)
    print(message)

def correct_for_timezone(hour):
  if hour + timezoneDiff < 0 :
    return today + timedelta(days=1)
  elif hour + timezoneDiff > 24:
    return today - timedelta(days=1)  
  else:
    return today

def main():
  for user in targetsInfo:
    commited = False
    jsonObject = get_user_github_events(user["username"])
    for key in jsonObject:
      eventType = key["type"]
      date = key["created_at"][:LAST_DATE_CHAR_INDEX]
      hour = int(key["created_at"][FIRST_HOUR_CHAR_INDEX: LAST_HOUR_CHAR_INDEX])
      todayCorrected = correct_for_timezone(hour)
      if eventType == "PushEvent" and date == str(todayCorrected):
        commited = True
        break
    if not commited:
      build_users(user["username"], False, user["discordId"])
    else:
      build_users(user["username"], True, user["discordId"])
  save_users_activities()

main()
