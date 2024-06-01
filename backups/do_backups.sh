#!/bin/bash
backup_dir="/backups_storage"
export PGPASSWORD=$CREATE_ROLES_SCRIPT_CREATOR_PASSWORD
sleep_time=$(($BACKUP_FREQUENCY_IN_HOURS * 3600))
get_current_date_time() {
    date '+%Y-%m-%d_%H:%M:%S'
}

count_backups() {
    find "$backup_dir" -mindepth 1 -maxdepth 1 | wc -l
}

find_oldest_backup() {
    ls "$backup_dir" --sort=time | tail -n 1
}

do_backup() {
    last_backup_name="$(get_current_date_time)"
    pg_dump -U "$BACKUP_USER" -h "$DB_HOSTNAME" -p "$HAPROXY_PRIMARY_PORT" -d "$BACKUP_DB_NAME" -f "$backup_dir/$last_backup_name"
}
remove_old_backups() {
    :
    while [[ "$(count_backups)" -gt "$MAX_BACKUPS_NUMBER" ]]; do
        oldest_backup="$(find_oldest_backup)"
        rm -rf "$backup_dir/$oldest_backup"
    done
}

while [[ true ]]; do
    start_time=$(date +%s)
    for ((i = 0; i < $MAX_BACKUP_ATTEMPTS; i++)); do
        do_backup && break
        rm -rf "$backup_dir/$last_backup_name" 2>/dev/null
        sleep $BACKUP_COOLDOWN_ON_FAILURE
    done
    real_sleep_time=$sleep_time
    if [[ $? -eq 0 ]]; then
        end_time=$(date +%s)
        real_sleep_time=$((sleep_time - (end_time - start_time)))
    fi
    remove_old_backups
    echo "now sleeping for $real_sleep_time seconds"
    sleep $real_sleep_time
done
