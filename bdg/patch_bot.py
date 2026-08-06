import re

with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add fs and path imports if not present
if "const fs = require('fs');" not in content:
    content = "const fs = require('fs');\nconst path = require('path');\n" + content

# Add loadData and saveData functions before STORAGE section
storage_code = """
// ============================================================
//  PERSISTENT STORAGE (bot_data.json)
// ============================================================
const DATA_FILE = path.join(__dirname, 'bot_data.json');

function loadData() {
    try {
        if (fs.existsSync(DATA_FILE)) {
            const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
            if (data.userTokens) userTokens = data.userTokens;
            if (data.autobetCfg) autobetCfg = data.autobetCfg;
            if (data.profitTrack) profitTrack = data.profitTrack;
            if (data.GLOBAL_TOKEN) GLOBAL_TOKEN = data.GLOBAL_TOKEN;
            if (data.usersAccess) usersAccess = data.usersAccess;
            if (data.keyStore) keyStore = data.keyStore;
            if (data.adminPasswords) adminPasswords = data.adminPasswords;
            if (data.stats) stats = data.stats;
            if (data.userCreds) userCreds = data.userCreds;
            console.log("✅ Data loaded from bot_data.json");
        }
    } catch (e) {
        console.error("❌ Error loading bot_data.json:", e.message);
    }
}

function saveData() {
    try {
        const data = {
            userTokens,
            autobetCfg,
            profitTrack,
            GLOBAL_TOKEN,
            usersAccess,
            keyStore,
            adminPasswords,
            stats,
            userCreds
        };
        fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf8');
    } catch (e) {
        console.error("❌ Error saving bot_data.json:", e.message);
    }
}

// Load data at startup
loadData();
// Auto save every 30 seconds
setInterval(saveData, 30 * 1000);
"""

content = content.replace("// ============================================================\n//  STORAGE\n// ============================================================", storage_code + "\n// ============================================================\n//  STORAGE\n// ============================================================")

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched bot.js!")
