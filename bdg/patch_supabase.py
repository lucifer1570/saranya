with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove old local storage code (loadData / saveData / DATA_FILE / setInterval)
old_storage_code = """// ============================================================
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
setInterval(saveData, 30 * 1000);"""

# Replace with Supabase client initialization and async load/save functions
new_supabase_code = """// ============================================================
//  SUPABASE PERSISTENT STORAGE
// ============================================================
const { createClient } = require('@supabase/supabase-js');
const SUPABASE_URL = process.env.SUPABASE_URL || "";
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY || "";

let supabase = null;
if (SUPABASE_URL && SUPABASE_KEY) {
    supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
    console.log("✅ Supabase client initialized");
} else {
    console.log("⚠️ Supabase credentials not found in environment variables. Running with memory-only storage.");
}

async function loadDataFromSupabase() {
    if (!supabase) return;
    try {
        const { data, error } = await supabase.from('bot_kv_store').select('*');
        if (error) {
            console.error("❌ Error loading from Supabase:", error.message);
            return;
        }
        if (data && data.length > 0) {
            data.forEach(row => {
                const k = row.key;
                const v = row.value;
                if (k === 'userTokens') userTokens = v || {};
                if (k === 'autobetCfg') autobetCfg = v || {};
                if (k === 'profitTrack') profitTrack = v || {};
                if (k === 'GLOBAL_TOKEN') GLOBAL_TOKEN = v || "";
                if (k === 'usersAccess') usersAccess = v || {};
                if (k === 'keyStore') keyStore = v || {};
                if (k === 'adminPasswords') adminPasswords = v || {};
                if (k === 'stats') stats = v || {};
                if (k === 'userCreds') userCreds = v || {};
            });
            console.log("✅ Data successfully loaded from Supabase");
        }

        // Load game results
        const { data: gData, error: gError } = await supabase
            .from('game_results')
            .select('*')
            .order('created_at', { ascending: false })
            .limit(500);
        
        if (!gError && gData) {
            gameResults = gData.map(r => ({
                time: r.created_at,
                userId: r.user_id,
                period: r.period,
                betType: r.bet_type,
                number: r.number,
                size: r.size,
                color: r.color,
                outcome: r.outcome,
                profit: Number(r.profit)
            }));
            console.log(`✅ Loaded ${gameResults.length} game results from Supabase`);
        }
    } catch (e) {
        console.error("❌ Exception loading from Supabase:", e.message);
    }
}

async function saveDataToSupabase() {
    if (!supabase) return;
    try {
        const storeData = [
            { key: 'userTokens', value: userTokens },
            { key: 'autobetCfg', value: autobetCfg },
            { key: 'profitTrack', value: profitTrack },
            { key: 'GLOBAL_TOKEN', value: GLOBAL_TOKEN },
            { key: 'usersAccess', value: usersAccess },
            { key: 'keyStore', value: keyStore },
            { key: 'adminPasswords', value: adminPasswords },
            { key: 'stats', value: stats },
            { key: 'userCreds', value: userCreds }
        ];

        for (const item of storeData) {
            await supabase.from('bot_kv_store').upsert(item, { onConflict: 'key' });
        }
    } catch (e) {
        console.error("❌ Error saving KV to Supabase:", e.message);
    }
}

// Load data at startup (non-blocking)
if (supabase) {
    loadDataFromSupabase();
    // Auto save KV every 30 seconds
    setInterval(saveDataToSupabase, 30 * 1000);
}
"""

if old_storage_code in content:
    content = content.replace(old_storage_code, new_supabase_code)
else:
    # If exact old storage code search fails, replace starting from PERSISTENT STORAGE comment
    import re
    content = re.sub(r'// ====================================\s*//\s+PERSISTENT STORAGE.*?setInterval\(saveData, 30 \* 1000\);', new_supabase_code, content, flags=re.DOTALL)

# Update logGameResult to insert into Supabase game_results table
old_logger = re.search(r'function logGameResult\([^)]*\)\s*\{.*?\n\}\s*\n', content, re.DOTALL)

new_logger = """
function logGameResult(period, betType, number, color, outcome, profit, userId) {
    if (!gameResults) gameResults = [];
    
    const numStr = String(number !== undefined ? number : "-");
    const size = getNumberSize(numStr);
    const resolvedColor = (color && color !== "-") ? color : getNumberColor(numStr);

    const record = {
        time: new Date().toISOString(),
        userId: userId ? String(userId) : "SYSTEM",
        period: period || "UNKNOWN",
        betType: betType || "BET",
        number: numStr,
        size: size,
        color: resolvedColor,
        outcome: outcome, // 'WIN' or 'LOSS'
        profit: Number(profit) || 0
    };

    gameResults.unshift(record);

    // Keep exactly latest 500 results in memory
    if (gameResults.length > 500) {
        gameResults = gameResults.slice(0, 500);
    }

    // Save asynchronously to Supabase
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
            if (error) console.error("❌ Error inserting game result into Supabase:", error.message);
        });
    }

    // Also save KV store state
    saveDataToSupabase();
}
"""

if old_logger:
    content = content.replace(old_logger.group(0), new_logger)

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated bot.js with Supabase storage!")
