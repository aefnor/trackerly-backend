@echo off
setlocal

:: Define variables
set ALEMBIC=alembic
set DATABASE_URL=postgresql://fooduser:foodpass@localhost:5432/foodtracker

:: Check for command argument
if "%~1"=="" (
    echo "Usage: alembic_commands.bat [command]"
    echo "Commands:"
    echo "  create          Create a new migration"
    echo "  upgrade         Upgrade to the latest migration"
    echo "  downgrade       Downgrade to the previous migration"
    echo "  history         Show the migration history"
    echo "  revision        Create a new migration script with a message"
    exit /b 1
)

:: Handle commands
if "%~1"=="create" (
    %ALEMBIC% revision --autogenerate -m "New migration"
)

if "%~1"=="upgrade" (
    %ALEMBIC% upgrade head
)

if "%~1"=="downgrade" (
    %ALEMBIC% downgrade -1
)

if "%~1"=="history" (
    %ALEMBIC% history --verbose
)

if "%~1"=="revision" (
    if "%~2"=="" (
        echo "Please provide a message for the migration."
        exit /b 1
    )
    %ALEMBIC% revision -m "%~2"
)

endlocal
