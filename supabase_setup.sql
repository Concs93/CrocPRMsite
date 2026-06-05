-- ============================================================
-- MVP Cards Voting — Supabase setup
-- ============================================================
-- Run this in: Supabase → SQL Editor → New query → paste → Run
--
-- Schema overview:
--   • mvp_aggregate  — one row per card, holds the 5 rating counters
--   • mvp_comments   — anonymous comments (500 char cap, optional username)
--
-- Two RPC functions handle vote +1 / -1 atomically:
--   • vote_add(card_id, rating)
--   • vote_remove(card_id, rating)
--
-- Anonymous (no auth). Per-user dedup is via browser localStorage on the
-- client side — clearing cache allows re-voting (deliberate, user choice).
-- ============================================================


-- ── Tables ─────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS mvp_aggregate (
    card_id INT PRIMARY KEY,
    useless INT NOT NULL DEFAULT 0,
    weak    INT NOT NULL DEFAULT 0,
    ok      INT NOT NULL DEFAULT 0,
    strong  INT NOT NULL DEFAULT 0,
    meta    INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mvp_comments (
    id          BIGSERIAL PRIMARY KEY,
    card_id     INT NOT NULL,
    content     TEXT NOT NULL CHECK (length(content) BETWEEN 1 AND 500),
    username    TEXT,                       -- nullable: empty = anonymous
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_mvp_comments_card_id
    ON mvp_comments (card_id, created_at DESC);


-- ── RPC functions (atomic increments) ──────────────────────────

CREATE OR REPLACE FUNCTION vote_add(p_card_id INT, p_rating TEXT)
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    IF p_rating NOT IN ('useless','weak','ok','strong','meta') THEN
        RAISE EXCEPTION 'Invalid rating: %', p_rating;
    END IF;

    INSERT INTO mvp_aggregate (card_id) VALUES (p_card_id)
        ON CONFLICT (card_id) DO NOTHING;

    EXECUTE format(
        'UPDATE mvp_aggregate SET %I = %I + 1, updated_at = NOW() WHERE card_id = $1',
        p_rating, p_rating
    ) USING p_card_id;
END;
$$;

CREATE OR REPLACE FUNCTION vote_remove(p_card_id INT, p_rating TEXT)
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    IF p_rating NOT IN ('useless','weak','ok','strong','meta') THEN
        RAISE EXCEPTION 'Invalid rating: %', p_rating;
    END IF;

    EXECUTE format(
        'UPDATE mvp_aggregate SET %I = GREATEST(%I - 1, 0), updated_at = NOW() WHERE card_id = $1',
        p_rating, p_rating
    ) USING p_card_id;
END;
$$;


-- ── Row Level Security ─────────────────────────────────────────
-- Anonymous users can:
--   • SELECT from mvp_aggregate (read counts)
--   • SELECT from mvp_comments  (read comments)
--   • INSERT into mvp_comments  (write a comment)
--   • CALL vote_add / vote_remove RPCs (handled via SECURITY DEFINER)
-- They cannot UPDATE or DELETE anything directly.

ALTER TABLE mvp_aggregate ENABLE ROW LEVEL SECURITY;
ALTER TABLE mvp_comments  ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "anon read aggregate" ON mvp_aggregate;
CREATE POLICY "anon read aggregate"
    ON mvp_aggregate FOR SELECT
    TO anon
    USING (true);

DROP POLICY IF EXISTS "anon read comments" ON mvp_comments;
CREATE POLICY "anon read comments"
    ON mvp_comments FOR SELECT
    TO anon
    USING (true);

DROP POLICY IF EXISTS "anon insert comments" ON mvp_comments;
CREATE POLICY "anon insert comments"
    ON mvp_comments FOR INSERT
    TO anon
    WITH CHECK (
        length(content) BETWEEN 1 AND 500
    );


-- ── Grants ─────────────────────────────────────────────────────
-- The RPC functions are SECURITY DEFINER, so they bypass RLS to do
-- their inserts/updates. We still need to allow anon to CALL them.

GRANT EXECUTE ON FUNCTION vote_add(INT, TEXT)    TO anon;
GRANT EXECUTE ON FUNCTION vote_remove(INT, TEXT) TO anon;


-- ── Done. Verify with: ─────────────────────────────────────────
-- SELECT * FROM mvp_aggregate;
-- SELECT * FROM mvp_comments;
-- SELECT vote_add(4123, 'meta');     -- Eddga Card gets 1 "meta" vote
-- SELECT * FROM mvp_aggregate WHERE card_id = 4123;
-- SELECT vote_remove(4123, 'meta');  -- removes it
