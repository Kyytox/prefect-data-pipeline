# Setup Scripts for Prefect Data Pipeline

This directory contains scripts for setting up your data engineering environment.

## Available Scripts

- `setup.sh` - Main setup script (Bash version)
- `simple_setup.sh` - Simple setup script (POSIX shell compatible)
- `install_postgresql.sh` - PostgreSQL installation script
- `init_database.sh` - Database initialization script
- `install_dependencies.sh` - Dependencies installation script
- `cleanup.sh` - Environment cleanup script

## Troubleshooting

If you encounter the error `setup/setup.sh: Syntax error: "(" unexpected`, it means your shell doesn't support Bash arrays. Try using `simple_setup.sh` instead:

```bash
cd /path/to/your/project
chmod +x ./setup/simple_setup.sh
./setup/simple_setup.sh
```

## Manual Setup

If scripts are not working, you can run the steps manually:

1. Install PostgreSQL:
   ```bash
   sudo apt update
   sudo apt install -y postgresql postgresql-contrib
   ```

2. Initialize the database:
   ```bash
   sudo -u postgres psql -f create_db.sql
   sudo -u postgres psql -f create_table.sql
   ```

3. Install dependencies:
   ```bash
   pixi install
   ```

## Fixing Script Permissions

If you get "Permission denied" errors, make the scripts executable:

```bash
chmod +x ./setup/*.sh
```
