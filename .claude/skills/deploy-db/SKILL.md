---
name: deploy-db
description: Start PostgreSQL database and run schema setup for the memory system
allowed-tools:
  - Bash
---

# Deploy Database

Start the PostgreSQL + pgvector database and ensure the schema is initialized.

## Steps

1. Check if Docker is running:
```bash
docker info > /dev/null 2>&1 && echo "Docker running" || echo "Docker not running"
```

2. Start the database:
```bash
docker-compose up -d
```

3. Wait for health check:
```bash
docker-compose exec db pg_isready -U quantum -d quantum_claude
```

4. Verify schema exists:
```bash
docker-compose exec db psql -U quantum -d quantum_claude -c "\dt public.*"
```

5. If tables are missing, the init scripts in `supabase/setup/` run automatically on first start. If needed manually:
```bash
docker-compose exec db psql -U quantum -d quantum_claude -f /docker-entrypoint-initdb.d/001_init.sql
```

## Connection Details

- Host: localhost
- Port: 5432
- User: quantum
- Password: quantum
- Database: quantum_claude

## Troubleshooting

- If port 5432 is in use: `lsof -i :5432` to find the conflicting process
- To reset completely: `docker-compose down -v && docker-compose up -d`
