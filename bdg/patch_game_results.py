import re

with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add gameResults to storage data object if not present
if "gameResults" not in content:
    # Add gameResults variable
    content = content.replace("let userStates = {};", "let userStates = {};\nlet gameResults = [];\n")

    # Add gameResults to loadData
    load_target = "if (data.userCreds) userCreds = data.userCreds;"
    load_replacement = load_target + "\n            if (data.gameResults) gameResults = data.gameResults;"
    content = content.replace(load_target, load_replacement)

    # Add gameResults to saveData
    save_target = "            userCreds"
    save_replacement = "            userCreds,\n            gameResults"
    content = content.replace(save_target, save_replacement)

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully added gameResults storage!")
