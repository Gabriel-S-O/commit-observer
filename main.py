import requests
import json
import datetime

DISCORD_EMOJI_WRONG = ":no_entry_sign:"
DISCORD_EMOJI_RIGHT = ":white_check_mark:"

FIRST_DATE_CHAR_INDEX = 0
LAST_DATE_CHAR_INDEX = 10

today = str(datetime.date.today())


# put here your friends github usernames and their discord id's

peopleInfo = [
  {"username": "", "discordId": ""},
  {"username": "", "discordId": ""}
]

monkeysObject = []

messages = []

class Monkey(object):
  def __init__ (self, name, commited, discordId):
    self.name = name
    self.commited = "DID COMMIT" if commited else "DID NOT COMMIT"
    self.discordId = discordId


def get_monkey_github_events(monkey):
  r = requests.get("https://api.github.com/users/{monkey}/events".format(monkey = monkey))
  return json.loads(r.text)

def build_monkeys(monkeyName, commited, discordId):
  monkey = Monkey(monkeyName, commited, discordId)
  monkeysObject.append(monkey)

def save_monkeys_activities():
  for monkeyObject in monkeysObject:
    emoji = DISCORD_EMOJI_RIGHT if monkeyObject.commited == "DID COMMIT" else DISCORD_EMOJI_WRONG
    message = ("{} <@{}> **{}** {}".format(emoji, monkeyObject.discordId, monkeyObject.commited, emoji))
    messages.append(message)
    print(message)

def main():
  for monkey in peopleInfo:
    commited = False
    jsonObject = get_monkey_github_events(monkey["username"])
    for key in jsonObject:
      eventType = key["type"]
      isToday = key["created_at"][FIRST_DATE_CHAR_INDEX : LAST_DATE_CHAR_INDEX]
      if eventType == "PushEvent" and isToday == today:
        commited = True
        break
    if not commited:
      build_monkeys(monkey["username"], False, monkey["discordId"])
    else:
      build_monkeys(monkey["username"], True, monkey["discordId"])
  save_monkeys_activities()

main()