"""
BPU Nexus - Application Configuration

Purpose:
    This module contains the central configuration for the
    BPU Nexus backend.

Used by:
    Other backend modules that need access to application
    settings such as the database URL, API configuration,
    or security settings.

Security:
    Sensitive values are loaded from environment variables
    instead of being hardcoded into Python source code.

If changing later:
    Add new environment variables to the Settings class.
    Do not hardcode passwords, API keys, database credentials,
    or other secrets in application code.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from the .env file.

    Pydantic validates the values and converts them to the
    appropriate Python types.

    Example:

        API_PORT=8000

    becomes:

        settings.api_port

    with the value:

        8000
    """

    # --------------------------------------------------------
    # APPLICATION
    # --------------------------------------------------------

    # Name of our application.
    app_name: str = "BPU Nexus"

    # Current environment.
    #
    # Possible environments will eventually include:
    # development
    # testing
    # production
    app_env: str = "development"

    # --------------------------------------------------------
    # API SERVER
    # --------------------------------------------------------

    # Network interface used by the FastAPI server.
    api_host: str = "0.0.0.0"

    # Port used by the FastAPI server.
    api_port: int = 8000

    # --------------------------------------------------------
    # SECURITY
    # --------------------------------------------------------

    # Secret used by backend security mechanisms.
    #
    # No default value is provided intentionally.
    # The application should receive this value from .env.
    secret_key: str

    # --------------------------------------------------------
    # DATABASE
    # --------------------------------------------------------

    # Complete PostgreSQL connection URL.
    #
    # We keep the complete URL in configuration so the rest
    # of the application does not need to know individual
    # database credentials.
    database_url: str

    # --------------------------------------------------------
    # JWT AUTHENTICATION
    # --------------------------------------------------------

    # Secret key used to sign JWT tokens.
    jwt_secret_key: str

    # JWT signing algorithm.
    jwt_algorithm: str = "HS256"

    # Token lifetime in minutes.
    jwt_access_token_expire_minutes: int = 60

    class Config:
        """
        Pydantic configuration.

        env_file:
            Tells Pydantic to load variables from .env.

        case_sensitive:
            Allows environment variable names such as
            DATABASE_URL to map to database_url.
        """

        env_file = ".env"
        case_sensitive = False


# Create one shared configuration object.
#
# Other parts of BPU Nexus will import this object instead
# of reading .env directly.
settings = Settings()
