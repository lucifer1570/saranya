with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

new_prediction_code = """
// ============================================================
//  LUCIFER AI – ONLY SIZE PREDICTION STRATEGY
// ============================================================
function getNumInfo(item) {
    const n = parseInt(item.number || item.winNumber || 0);
    const size = n >= 5 ? "BIG" : "SMALL";
    let color = "UNKNOWN";
    if (n === 0) color = "RED";
    else if (n === 5) color = "GREEN";
    else if ([1, 3, 7, 9].includes(n)) color = "GREEN";
    else if ([2, 4, 6, 8].includes(n)) color = "RED";
    return { n, size, color };
}

function decidePrediction(list) {
    if (!list || list.length < 20) return null;

    const currentItem = list[0];
    const currentNum = parseInt(currentItem.number || currentItem.winNumber || 0);

    let matches = [];

    // Scan history for previous occurrences of currentNum
    // list[0] is most recent. Previous occurrences are at i >= 1.
    // The result that followed occurrence at i is at i - 1.
    for (let i = 1; i < list.length - 1; i++) {
        const pastItem = list[i];
        const pastNum = parseInt(pastItem.number || pastItem.winNumber || 0);
        if (pastNum === currentNum) {
            const nextItem = list[i - 1]; // Result that followed immediately after
            const nextInfo = getNumInfo(nextItem);
            matches.push({
                period: nextItem.issueNumber,
                ...nextInfo
            });
        }
    }

    // Require at least 3 matches
    if (matches.length < 3) return null;

    // Take the 3 most recent matches
    const top3 = matches.slice(0, 3);

    const size1 = top3[0].size;
    const size2 = top3[1].size;
    const size3 = top3[2].size;

    // Check if all 3 sizes are identical
    if (size1 === size2 && size2 === size3) {
        const c1 = top3[0].color;
        const c2 = top3[1].color;
        const c3 = top3[2].color;

        // Colors must NOT be all the same
        if (!(c1 === c2 && c2 === c3)) {
            const predictedSize = size1 === "BIG" ? "SMALL" : "BIG";
            return {
                type: 'SIZE',
                val: predictedSize,
                history: `${size1[0]},${size2[0]},${size3[0]} (3 Matches)`
            };
        }
    }

    return null;
}
"""

# Replace ResultAnalyzer and old decidePrediction with new prediction logic
import re

# Find where decidePrediction starts
if "function decidePrediction" in content:
    # We can replace from start of ResultAnalyzer or decidePrediction to updateAfterResult
    start_idx = content.find("class ResultAnalyzer")
    if start_idx == -1:
        start_idx = content.find("function decidePrediction")
    
    end_idx = content.find("// 1. updateAfterResult")
    if end_idx != -1:
        content = content[:start_idx] + new_prediction_code + "\n\n" + content[end_idx:]

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated prediction strategy in bot.js!")
