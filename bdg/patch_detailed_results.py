import re

with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

new_logger = """
// ============================================================
//  GAME RESULTS LOGGER (Detailed 500 records)
// ============================================================
function getNumberColor(num) {
    const n = parseInt(num);
    if (isNaN(n)) return "Unknown";
    if (n === 0) return "Red/Violet";
    if (n === 5) return "Green/Violet";
    if ([1, 3, 7, 9].includes(n)) return "Green";
    if ([2, 4, 6, 8].includes(n)) return "Red";
    return "Unknown";
}

function getNumberSize(num) {
    const n = parseInt(num);
    if (isNaN(n)) return "Unknown";
    return n >= 5 ? "Big" : "Small";
}

function logGameResult(period, betType, number, color, outcome, profit, userId) {
    if (!gameResults) gameResults = [];
    
    const numStr = String(number !== undefined ? number : "-");
    const size = getNumberSize(numStr);
    const resolvedColor = (color && color !== "-") ? color : getNumberColor(numStr);

    gameResults.unshift({
        time: new Date().toISOString(),
        userId: userId || "SYSTEM",
        period: period || "UNKNOWN",
        betType: betType || "BET",
        number: numStr,
        size: size,
        color: resolvedColor,
        outcome: outcome, // 'WIN' or 'LOSS'
        profit: profit
    });

    // Keep exactly latest 500 results
    if (gameResults.length > 500) {
        gameResults = gameResults.slice(0, 500);
    }
    saveData();
}
"""

if "function logGameResult" in content:
    content = re.sub(r'function logGameResult\([^)]*\)\s*\{.*?\n\}\s*\n', new_logger, content, flags=re.DOTALL)
else:
    content = new_logger + "\n" + content

# Update 📊 Game Results command
new_cmd = """
            if(text==="📊 Game Results") {
                if (!gameResults || gameResults.length === 0) return send(OWNER_ID, "No game results stored yet.");
                let report = "🎮 LATEST GAME RESULTS (Showing last 15 of " + gameResults.length + ")\n\\n";
                gameResults.slice(0, 15).forEach((r, idx) => {
                    report += `${idx+1}. Period: ${r.period}\\n`;
                    report += `   Num: ${r.number} | Size: ${r.size} | Color: ${r.color}\\n`;
                    report += `   Outcome: ${r.outcome} (₹${r.profit >= 0 ? '+' : ''}${r.profit})\\n`;
                    report += `   ------------------------\\n`;
                });
                return send(OWNER_ID, report);
            }
"""

if 'if(text==="📊 Game Results")' in content:
    content = re.sub(r'if\(text==="📊 Game Results"\)\s*\{.*?\n\s*\}', new_cmd.strip(), content, flags=re.DOTALL)
else:
    content = content.replace('if(text==="📊 All Status")    {', new_cmd + '\n            if(text==="📊 All Status")    {')

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated detailed game results storage!")
