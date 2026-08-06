with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add logGameResult in handleWin
win_target = 'async function handleWin(userId, chatId, actual, num, betLevel) {'
win_replacement = win_target + '\n    logGameResult("UNKNOWN", "BET", num, actual, "WIN", profit, userId);'
content = content.replace(win_target, win_replacement, 1)

# Add logGameResult in handleLoss
loss_target = 'async function handleLoss(userId, chatId, actual, num, betLevel) {'
loss_replacement = loss_target + '\n    logGameResult("UNKNOWN", "BET", num, actual, "LOSS", -amt, userId);'
content = content.replace(loss_target, loss_replacement, 1)

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully added logGameResult calls!")
