# Makefile for managing Alembic migrations

# Define variables
ALEMBIC=alembic
ALEMBIC_CONFIG=alembic.ini
DATABASE_URL=postgresql://fooduser:foodpass@localhost:5432/foodtracker

# Targets

# Default target
.PHONY: help
help:
	@echo "Makefile commands for Alembic"
	@echo ""
	@echo "Usage:"
	@echo "  make create         Create a new migration"
	@echo "  make upgrade        Upgrade to the latest migration"
	@echo "  make downgrade      Downgrade to the previous migration"
	@echo "  make history        Show the migration history"
	@echo "  make revision       Create a new migration script"
	@echo "  make run            Run alembic with a specified command"
	@echo ""

# Create a new migration based on changes in the models
.PHONY: create
create:
	@$(ALEMBIC) revision --autogenerate -m "New migration"

# Upgrade to the latest migration
.PHONY: upgrade
upgrade:
	@$(ALEMBIC) upgrade head

# Downgrade to the previous migration
.PHONY: downgrade
downgrade:
	@$(ALEMBIC) downgrade -1

# Show the migration history
.PHONY: history
history:
	@$(ALEMBIC) history --verbose

# Create a new migration with a specified message
.PHONY: revision
revision:
	@$(ALEMBIC) revision -m "$(message)"

# Run Alembic with a specified command
.PHONY: run
run:
	@$(ALEMBIC) $(command)

# Set the database URL as an environment variable
export DATABASE_URL=$(DATABASE_URL)

