# ---------------------------------------------------------
# Authentication & Authorization Dependencies
# ---------------------------------------------------------
#
# Handles:
#   1. Reading the JWT bearer token
#   2. Finding the authenticated user
#   3. Checking whether the user is an ADMIN
#
# BPU Nexus currently uses a simple role-based approach:
#
#     User.role == "ADMIN"
#
# We are no longer using:
#     user_roles
#     permissions
#     role_permissions
#
# ---------------------------------------------------------

import uuid

from fastapi import Depends, HTTPException, status

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session

from jose import JWTError, jwt

from app.core.config import settings
from app.db.dependencies import get_db
from app.models.user import User


# ---------------------------------------------------------
# Bearer Token Reader
# ---------------------------------------------------------
#
# Reads:
#
#     Authorization: Bearer <token>
#
# ---------------------------------------------------------

security = HTTPBearer()


# ---------------------------------------------------------
# GET CURRENT USER
# ---------------------------------------------------------
#
# Validates the JWT and returns the authenticated user.
#
# ---------------------------------------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db),
):
    """
    Return the currently authenticated user.
    """

    # -----------------------------------------------------
    # Extract JWT from Authorization header.
    # -----------------------------------------------------

    token = credentials.credentials

    try:

        # -------------------------------------------------
        # Decode and verify JWT.
        # -------------------------------------------------

        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        # -------------------------------------------------
        # Read user ID from the "sub" claim.
        # -------------------------------------------------

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token.",
            )

        # -------------------------------------------------
        # Convert the user ID into UUID.
        # -------------------------------------------------

        user_uuid = uuid.UUID(user_id)

    except (JWTError, ValueError):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
        )

    # -----------------------------------------------------
    # Find the user in the database.
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(User.id == user_uuid)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return user


# ---------------------------------------------------------
# REQUIRE ADMIN
# ---------------------------------------------------------
#
# Only users whose users.role is ADMIN can continue.
#
# Example database value:
#
#     users.role = "ADMIN"
#
# ---------------------------------------------------------

def require_admin(
    current_user: User = Depends(get_current_user),
):
    """
    Allow access only to ADMIN users.
    """

    if current_user.role != "ADMIN":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ADMIN role required.",
        )

    return current_user
