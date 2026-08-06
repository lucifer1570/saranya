with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

poller_code = """
// ============================================================
//  HIGH-FREQUENCY 200MS API POLLER & SUPABASE SYNC
// ============================================================
let lastKnownIssue = null;

async function pollAndStoreApiResults() {
    try {
        const list = await fetchList();
        if (list && list.length > 0) {
            const latest = list[0];
            const issueNumber = latest.issueNumber || latest.period;
            
            if (issueNumber && issueNumber !== lastKnownIssue) {
                lastKnownIssue = issueNumber;
                const num = parseInt(latest.number || latest.winNumber || 0);
                const size = num >= 5 ? "Big" : "Small";
                const color = (latest.colour || latest.color || (num === 0 ? "Red/Violet" : num === 5 ? "Green/Violet" : num % 2 === 0 ? "Red" : "Green"));

                // Check if already exists in memory gameResults
                if (!gameResults) gameResults = [];
                const exists = gameResults.some(r => r.period === issueNumber);

                if (!exists) {
                    const record = {
                        time: new Date().toISOString(),
                        userId: "SYSTEM_POLL",
                        period: String(issueNumber),
                        betType: "AUTO_SYNC",
                        number: String(num),
                        size: size,
                        color: color,
                        outcome: "DRAW",
                        profit: 0
                    };

                    gameResults.unshift(record);
                    if (gameResults.length > 500) {
                        gameResults = gameResults.slice(0, 500);
                    }

                    // Save to Supabase
                    if (supabase) {
                        supabase.from('game_results').insert({
                            user_id: record.userId,
                            period: record.period,
                            bet_type: record.betType,
                            number: record.number,
                            size: record.size,
                            color: record.color,
                            outcome: record.outcome,
                            profit: record.profit
                        }).then(({ error }) => {
                            if (error) {
                                // Ignore duplicate key errors if already inserted
                                if (!error.message.includes('duplicate key')) {
                                    console.error("❌ Supabase poll sync error:", error.message);
                                }
                            } else {
                                console.log(`[POLL SYNC] New period ${record.period} (Num: ${num}, Size: ${size}) saved to Supabase.`);
                            }
                        });
                    }
                }
            }
        }
    } catch (e) {
        // Suppress network jitter errors in poller
    }
}

// Start 200ms background poller after 3 seconds
setTimeout(() => {
    setInterval(pollAndStoreApiResults, 200);
    console.log("⚡ High-frequency 200ms API poller started!");
}, 3000);
"""

content = poller_code + "\n" + content

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully added 200ms API poller!")
