"""
BPU Nexus - Configuration Test

Purpose:
    Verifies that the application configuration is being
    loaded correctly from the .env file.

Why we have this file:
    Before connecting to PostgreSQL or starting FastAPI,
    we want to make sure our configuration system works.

Security:
    We intentionally DO NOT print the database password.
    Printing secrets to the terminal can expose them in
    shell history, logs, screenshots, or CI systems.

If changing later:
    When new configuration values are added to config.py,
    we can add safe verification here.
"""

# Import the shared configuration object.
#
# The settings object has already loaded values from .env.
from app.core.config import settings


# ------------------------------------------------------------
# APPLICATION CONFIGURATION
# ------------------------------------------------------------

# Verify that the application name was loaded.
print("App Name:", settings.app_name)


# Verify that the current environment was loaded.
print("Environment:", settings.app_env)


# Verify that the API port was loaded and converted to an int.
print("API Port:", settings.api_port)


# ------------------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------------------

# Verify that a database URL exists.
#
# IMPORTANT:
# We only print whether it exists.
# We NEVER print the complete DATABASE_URL because it
# contains the database password.
print("Database configured:", bool(settings.database_url))
