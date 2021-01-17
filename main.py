import requests
import lxml.html
import json
import math
import os

def getFileContents(path):
    file = open(path, "r", encoding='utf-8')
    contents = file.read()
    file.close()
    return contents

# Load config
config = json.loads(getFileContents("config.json"))

accounts = config["accounts"]
targetExp = config["target_exp"]
spellName = config["spell"]["name"]
spellExp = config["spell"]["exp"]
spellRunes = config["spell"]["runes"]

# Delete calculations if already present
if os.path.exists("calculations.txt"):
    os.remove("calculations.txt")

# Open file
file = open("calculations.txt", "a")

# Loop through accounts
for account in accounts:
    print(f"Calculating casts remaining for: {account}")

    apiUrl = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={account}"
    html_string = requests.get(apiUrl).content
    body = lxml.html.document_fromstring(html_string).find('body')
    text = body.text_content()

    levelData = text.splitlines()
    currentExp = int(levelData[7].split(',')[2])
    remainingExp = max(targetExp - currentExp, 0)
    castsRemaining = math.ceil(remainingExp / spellExp)


    print(f" <<<< Calculations for {account} >>>> ")
    print("")
    print(f"Current experience: {currentExp}")
    print(f"Target experience: {targetExp}")
    print(f"Remaining Experience: {remainingExp}")
    print()
    print(f"{spellName} casts remaining: {castsRemaining}")
    print("Runes required:")

    for rune, amount in spellRunes.items():
        print(f"  {rune.capitalize()} rune: {amount * castsRemaining}")

    print("-----------------------------------------")
    print()

    file.write(f" <<<< Calculations for {account} >>>> \n")
    file.write("\n")
    file.write(f"Current experience: {currentExp}\n")
    file.write(f"Target experience: {targetExp}\n")
    file.write(f"Remaining Experience: {remainingExp}\n")
    file.write("\n")
    file.write(f"{spellName} casts remaining: {castsRemaining}\n")
    file.write("Runes required:\n")

    for rune, amount in spellRunes.items():
        file.write(f"  {rune.capitalize()} rune: {amount * castsRemaining}\n")

    file.write("-----------------------------------------\n")
    file.write("\n")

# Close file
file.close()

print("Done!")

        

