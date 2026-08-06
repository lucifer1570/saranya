with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Update decidePrediction function to use gameResults (from Supabase/memory) combined with list
old_decide = """function decidePrediction(list) {
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
    }"""

new_decide = """function decidePrediction(list) {
    if (!list || list.length < 1) return null;

    // Use gameResults (fetched from Supabase database) combined with live list if available for deep historical scanning
    let combinedHistory = [];
    if (typeof gameResults !== 'undefined' && gameResults.length > 0) {
        combinedHistory = gameResults.map(r => ({
            issueNumber: r.period,
            number: r.number,
            winNumber: r.number
        }));
    }

    // If database history has fewer than 20 records, fall back or merge with live API list
    if (combinedHistory.length < 20 && list && list.length > 0) {
        combinedHistory = list;
    }

    if (combinedHistory.length < 20) return null;

    const currentItem = combinedHistory[0];
    const currentNum = parseInt(currentItem.number || currentItem.winNumber || 0);

    let matches = [];

    // Scan history for previous occurrences of currentNum
    for (let i = 1; i < combinedHistory.length - 1; i++) {
        const pastItem = combinedHistory[i];
        const pastNum = parseInt(pastItem.number || pastItem.winNumber || 0);
        if (pastNum === currentNum) {
            const nextItem = combinedHistory[i - 1]; // Result that followed immediately after
            const nextInfo = getNumInfo(nextItem);
            matches.push({
                period: nextItem.issueNumber || nextItem.period,
                ...nextInfo
            });
        }
    }"""

content = content.replace(old_decide, new_decide)

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated decidePrediction to use database history!")
