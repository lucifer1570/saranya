with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

bad_block = """            if(text==="📊 Game Results") {
                if (!gameResults || gameResults.length === 0) return send(OWNER_ID, "No game results stored yet.");
                let report = "🎮 LATEST GAME RESULTS (Showing last 15 of " + gameResults.length + ")

";
                gameResults.slice(0, 15).forEach((r, idx) => {
                    report += `${idx+1}. Period: ${r.period}
`;
                    report += `   Num: ${r.number} | Size: ${r.size} | Color: ${r.color}
`;
                    report += `   Outcome: ${r.outcome} (₹${r.profit >= 0 ? '+' : ''}${r.profit})
`;
                    report += `   ------------------------
`;
                });
                return send(OWNER_ID, report);
            });
                return send(OWNER_ID, report);
            }"""

good_block = """            if(text==="📊 Game Results") {
                if (!gameResults || gameResults.length === 0) return send(OWNER_ID, "No game results stored yet.");
                let report = "🎮 LATEST GAME RESULTS (Showing last 15 of " + gameResults.length + ")\\n\\n";
                gameResults.slice(0, 15).forEach((r, idx) => {
                    report += `${idx+1}. Period: ${r.period}\\n`;
                    report += `   Num: ${r.number} | Size: ${r.size} | Color: ${r.color}\\n`;
                    report += `   Outcome: ${r.outcome} (₹${r.profit >= 0 ? '+' : ''}${r.profit})\\n`;
                    report += `   ------------------------\\n`;
                });
                return send(OWNER_ID, report);
            }"""

if bad_block in content:
    content = content.replace(bad_block, good_block)
else:
    # Fallback search and replace using regex
    import re
    content = re.sub(r'if\(text==="📊 Game Results"\).*?return send\(OWNER_ID, report\);\s*\}\s*\}', good_block, content, flags=re.DOTALL)

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully fixed syntax error in bot.js!")
