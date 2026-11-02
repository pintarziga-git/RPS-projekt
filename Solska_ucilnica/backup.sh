#!/bin/sh
# Varnostna kopija baze. Dnevno ob 2h (crontab -e):  0 2 * * * /pot/do/projekta/backup.sh
cd "$(dirname "$0")"
. ./.env
mkdir -p backup
docker compose exec -T baza mariadb-dump -uroot -p"$MARIADB_ROOT_PASSWORD" "$DB_NAME" > backup/solska_$(date +%Y-%m-%d_%H%M).sql
find backup -name '*.sql' -mtime +14 -delete
