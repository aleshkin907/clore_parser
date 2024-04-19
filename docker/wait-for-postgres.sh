#!/bin/sh
# wait-for-postgres.sh

set -e

host="$DB_HOST"
port="$DB_PORT"
user="$DB_USER"
password="$DB_PASS"
database="$DB_NAME"

until PGPASSWORD="$password" psql -h "$host" -p "$port" -U "$user" -d "$database" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec "$@"