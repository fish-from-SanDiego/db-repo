#!/bin/bash
script_dir="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
python -u "$script_dir/init.py" || exit 1
python -u "$script_dir/migrate.py" || exit 1
python -u "$script_dir/generation_files/$(cat "$(dirname $script_dir)/util_files/max_migration_version.txt")/generate.py"

# if [[ "$CREATE_ROLES" == 'true' ]]; then
#     "$script_dir/create_roles.sh"
# fi
