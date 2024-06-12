CREATE EXTENSION IF NOT EXISTS btree_gin;
CREATE INDEX IF NOT EXISTS client_name_index ON clients USING GIN(client_name);