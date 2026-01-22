#!/bin/bash
set -e

echo "Waiting for database..."
for i in {1..30}; do
  if pg_isready -h postgres -U admin -d translator_db > /dev/null 2>&1; then
    echo "Database is ready!"
    break
  fi
  echo "Waiting for database... ($i/30)"
  sleep 2
done

echo "Running database migrations..."
cd /app/backend

# Override alembic.ini database URL with environment variables
export DATABASE_URL="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
alembic -x dbUrl="$DATABASE_URL" upgrade head

echo "Starting application..."
cd /app
exec uvicorn app.run:app --host 0.0.0.0 --port 8000
