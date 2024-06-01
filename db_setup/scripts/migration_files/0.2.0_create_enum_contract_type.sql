DO $$ BEGIN
    CREATE TYPE type_of_contract AS ENUM ( 'rent', 'purchase', 'sale' );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;