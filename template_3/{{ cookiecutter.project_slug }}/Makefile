.PHONY: sql-install
sql-install:
	@echo "Installing PostgreSQL..."
	@chmod +x setup_postegre.sh
	@./setup_postegre.sh


.PHONY: db-init
db-init:
	@echo "Initializing Database..."
	@echo 
	@sudo -u postgres psql -f create_db.sql
	@echo "Database initialized."
	@echo 
	@echo "Creating Table..."
	@echo
	@sudo -u postgres psql -f create_table.sql


.PHONY: setup-install
setup-install:
	@echo "Setting up environment variables..."
	@set -a
	@source .env
	@set +a
	@echo "Environment variables set."
	@echo
	@echo "Installing - Activation of Pixi..."
	@echo 
	@pixi install
	@pixi shell
	@echo "Pixi installed and shell activated."
	@echo


.PHONY: pixi-clean
pixi-clean:
	@echo "Cleaning - Deactivation of Pixi..."
	@echo 
	@exit
	@pixi clean