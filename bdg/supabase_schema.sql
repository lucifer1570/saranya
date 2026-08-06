-- ============================================================
-- Supabase Database Schema for Telegram Autobet Bot
-- ============================================================

-- 1. Game Results Table (Stores latest 500+ game results)
CREATE TABLE IF NOT EXISTS game_results (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id TEXT,
    period TEXT,
    bet_type TEXT,
    number TEXT,
    size TEXT,
    color TEXT,
    outcome TEXT,
    profit NUMERIC
);

-- Index for fast querying and sorting by latest
CREATE INDEX IF NOT EXISTS idx_game_results_created ON game_results (created_at DESC);

-- 2. User State & KV Store Table (Stores user tokens, config, access expiry, stats, etc.)
CREATE TABLE IF NOT EXISTS bot_kv_store (
    key TEXT PRIMARY KEY,
    value JSONB,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
