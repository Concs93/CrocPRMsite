-- ============================================================
-- Add comment counts view
-- ============================================================
-- Run this in: Supabase → SQL Editor → New query → paste → Run
-- This adds a lightweight view so the page can show "(N comments)"
-- per card without querying each one individually.
-- ============================================================

CREATE OR REPLACE VIEW mvp_comment_counts AS
    SELECT card_id, COUNT(*)::INT AS count
    FROM mvp_comments
    GROUP BY card_id;

GRANT SELECT ON mvp_comment_counts TO anon;

-- Verify:
-- SELECT * FROM mvp_comment_counts;
