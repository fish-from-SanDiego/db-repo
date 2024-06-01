#!/bin/bash
export PGPASSWORD=$CREATE_ROLES_SCRIPT_CREATOR_PASSWORD
connect_psql() {
    psql $CREATE_ROLES_SCRIPT_DB_NAME -U $CREATE_ROLES_SCRIPT_CREATOR_NAME -p $HAPROXY_PRIMARY_PORT -h $DB_HOSTNAME -b "$@"
}

get_query_text() {
    local rolname="$1"
    local query_main_text="$2"
    local beginning
    read -r -d '' query_text <<-EOQ
DO
\$do\$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = '${rolname}') THEN
      RAISE NOTICE 'Role ${rolname} already exists. Skipping.';
   ELSE
      ${query_main_text}
   END IF;
END
\$do\$;
EOQ
    echo "$query_text"
}
if [[ -z "$CREATE_ROLES_SCRIPT_DB_NAME" ]] || [[ -z "$CREATE_ROLES_SCRIPT_CREATOR_NAME" ]]; then
    echo 'error: script executor or db is name unknown'
    exit 1
fi

if [[ -z "$READER_PASSWORD" ]]; then
    echo 'error: reader password is unknown'
else
    connect_psql -c "$(get_query_text "reader" "CREATE ROLE reader WITH LOGIN PASSWORD '$READER_PASSWORD'; GRANT CONNECT ON DATABASE $CREATE_ROLES_SCRIPT_DB_NAME TO reader; GRANT USAGE ON SCHEMA public TO reader; GRANT SELECT ON ALL TABLES IN SCHEMA public to reader;ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO reader;")"
fi

if [[ -z "$WRITER_PASSWORD" ]]; then
    echo 'error: writer password is unknown'
else
    connect_psql -c "$(get_query_text "writer" "CREATE ROLE writer WITH LOGIN PASSWORD '$WRITER_PASSWORD'; GRANT CONNECT ON DATABASE $CREATE_ROLES_SCRIPT_DB_NAME TO writer; GRANT USAGE ON SCHEMA public TO writer; GRANT SELECT, UPDATE, INSERT ON ALL TABLES IN SCHEMA public to writer;ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, UPDATE, INSERT ON TABLES TO writer;")"
fi

if [[ -z "$ANALYTIC_PASSWORD" ]] || [[ -z "$ANALYTIC_ROLE_TABLE_NAME" ]]; then
    echo 'error: analytic password or table name is unknown'
else
    connect_psql -c "$(get_query_text "analytic" "CREATE ROLE analytic WITH LOGIN PASSWORD '$ANALYTIC_PASSWORD'; GRANT CONNECT ON DATABASE $CREATE_ROLES_SCRIPT_DB_NAME TO analytic; GRANT USAGE ON SCHEMA public TO analytic; GRANT SELECT ON $ANALYTIC_ROLE_TABLE_NAME to analytic;")"
fi

if [[ -z "$NOLOGIN_ROLE_NAME" ]]; then
    echo 'error: nologin role name is unknown'
else
    connect_psql -c "$(get_query_text "$NOLOGIN_ROLE_NAME" "CREATE ROLE $NOLOGIN_ROLE_NAME WITH NOLOGIN; GRANT CONNECT ON DATABASE $CREATE_ROLES_SCRIPT_DB_NAME TO $NOLOGIN_ROLE_NAME; GRANT USAGE ON SCHEMA public TO $NOLOGIN_ROLE_NAME; GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public to $NOLOGIN_ROLE_NAME; ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, UPDATE, INSERT, DELETE ON TABLES TO $NOLOGIN_ROLE_NAME;")"
    IFS=',' read -r -a usernames <<<"$CRUD_USER_NAMES"
    IFS=',' read -r -a passwords <<<"$CRUD_USER_PASSWORDS"
    if [ ${#usernames[@]} -ne ${#passwords[@]} ]; then
        echo 'error: password and username counts are not equal'
    else
        for i in "${!usernames[@]}"; do
            username="${usernames[$i]}"
            password="${passwords[$i]}"
            connect_psql -c "$(get_query_text "$username" "CREATE ROLE $username WITH LOGIN PASSWORD '$password'; GRANT $NOLOGIN_ROLE_NAME to $username;")"
        done
    fi
fi
