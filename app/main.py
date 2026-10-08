# ---------------------------------------------------------
# BPU Nexus - FastAPI Application
# ---------------------------------------------------------
#
# Main entry point for the BPU Nexus backend.
#
# Current scope:
#
#     Authentication
#     Role Management
#
# Role Management:
#
#     GET    /api/roles/
#     GET    /api/roles/{role_id}
#     POST   /api/roles/
#     PUT    /api/roles/{role_id}
#     DELETE /api/roles/{role_id}
#
# Only ADMIN users can manage roles.
#
# ---------------------------------------------------------

from fastapi import Depends, FastAPI

from sqlalchemy import text

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.api.auth import router as auth_router

from app.api.roles import router as roles_router


# ---------------------------------------------------------
# Create FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="BPU Nexus API",
    description="Backend API for BPU Nexus authentication and role management.",
    version="1.0.0",
)


# ---------------------------------------------------------
# Register Authentication Routes
# ---------------------------------------------------------
#
# Provides:
#
#     POST /api/auth/login
#
# ---------------------------------------------------------

app.include_router(auth_router)


# ---------------------------------------------------------
# Register Role Management Routes
# ---------------------------------------------------------
#
# Provides:
#
#     GET    /api/roles/
#     GET    /api/roles/{role_id}
#     POST   /api/roles/
#     PUT    /api/roles/{role_id}
#     DELETE /api/roles/{role_id}
#
# All role endpoints require ADMIN authentication.
#
# ---------------------------------------------------------

app.include_router(roles_router)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
#
# GET /health
#
# Confirms that the API is running.
#
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    """
    Return the current API health status.
    """

    return {
        "status": "ok",
        "service": "BPU Nexus API",
    }


# ---------------------------------------------------------
# Database Health Check
# ---------------------------------------------------------
#
# GET /health/db
#
# Confirms that FastAPI can communicate with PostgreSQL.
#
# ---------------------------------------------------------

@app.get("/health/db")
def database_health_check(
    db: Session = Depends(get_db),
):
    """
    Check the connection between FastAPI and PostgreSQL.
    """

    # -----------------------------------------------------
    # Execute a simple PostgreSQL query.
    # -----------------------------------------------------

    result = db.execute(text("SELECT 1"))

    # -----------------------------------------------------
    # Get the returned value.
    # -----------------------------------------------------

    value = result.scalar()

    return {
        "status": "ok",
        "database": "connected",
        "result": value,
    }
