-- Ҷадвалҳои базаи D1 «smm-bot». Аллакай сохта шудаанд; барои базаи нав:
--   npx wrangler d1 execute smm-bot --remote --file=schema.sql
CREATE TABLE IF NOT EXISTS deliveries (
    user_id     INTEGER NOT NULL,
    keyword_id  TEXT    NOT NULL,
    username    TEXT,
    first_name  TEXT,
    created_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, keyword_id)
);

CREATE TABLE IF NOT EXISTS comment_replies (
    user_id     INTEGER NOT NULL,
    keyword_id  TEXT    NOT NULL,
    replied_at  INTEGER NOT NULL,
    PRIMARY KEY (user_id, keyword_id)
);
