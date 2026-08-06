with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add a helper function to log game results
logger_func = """
// ============================================================
//  GAME RESULTS LOGGER
// ============================================================
function logGameResult(period, betType, number, color, outcome, profit, userId) {
    if (!gameResults) gameResults = [];
    gameResults.unshift({
        time: new Date().toISOString(),
        userId: userId || "SYSTEM",
        period: period,
        betType: betType,
        number: number,
        color: color,
        outcome: outcome, // 'WIN' or 'LOSS'
        profit: profit
    });
    // Keep last 500 results
    if (gameResults.length > 500) {
        gameResults = gameResults.slice(0, 500);
    }
    saveData();
}
"""

content = logger_func + "\n" + content

# Add command to view recent game results for Owner
cmd_code = """
            if(text==="📊 Game Results") {
                if (!gameResults || gameResults.length === 0) return send(OWNER_ID, "No game results stored yet.");
                let report = "🎮 RECENT GAME RESULTS (Last 15)\n\\n";
                gameResults.slice(0, 15).forEach((r, idx) => {
                    report += `${idx+1}. Period: ${r.period}\\n`;
                    report += `   User: ${r.userId} | Bet: ${r.betType}\\n`;
                    report += `   Result: ${r.outcome} (₹${r.profit >= 0 ? '+' : ''}${r.profit})\\n`;
                    report += `   ------------------------\\n`;
                });
                return send(OWNER_ID, report);
            }
"""

# Insert command into owner menu handler
content = content.replace('if(text==="📊 All Status")    {', cmd_code + '\n            if(text==="📊 All Status")    {')

# Also update owner menu keyboard to include "📊 Game Results"
keyboard_code = '["📊 All Status","🔑 Generate Key"]'
keyboard_replacement = '["📊 All Status","📊 Game Results"],\n                ["🔑 Generate Key"]'
content = content.replace(keyboard_code, keyboard_replacement)

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully added game logger and command!")
