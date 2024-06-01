DO $$ BEGIN
    CREATE TYPE item_condition AS ENUM ( 'new', 'used', 'slightly damaged', 'damaged', 'repaired', 'broken' );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;