# ---------------------------------------------------------
# Role API Routes
# ---------------------------------------------------------
#
# ADMIN users can:
#
#   - Create roles
#   - Read roles
#   - Update roles
#   - Delete roles
#
# When creating a role, an initial user account is also
# created for that role.
#
# ---------------------------------------------------------

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.models.role import Role

from app.models.user import User

from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
)

from app.api.dependencies import require_admin

from app.core.security import hash_password


# ---------------------------------------------------------
# Router Configuration
# ---------------------------------------------------------

router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"],
)


# ---------------------------------------------------------
# GET ALL ROLES
# ---------------------------------------------------------
#
# ADMIN only
#
# GET /api/roles/
# ---------------------------------------------------------

@router.get(
    "/",
    response_model=list[RoleResponse],
)
def get_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Return all available roles.
    """

    roles = (
        db.query(Role)
        .order_by(Role.name)
        .all()
    )

    return roles


# ---------------------------------------------------------
# GET ONE ROLE
# ---------------------------------------------------------
#
# ADMIN only
#
# GET /api/roles/{role_id}
# ---------------------------------------------------------

@router.get(
    "/{role_id}",
    response_model=RoleResponse,
)
def get_role(
    role_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Return one role by ID.
    """

    role = (
        db.query(Role)
        .filter(Role.id == role_id)
        .first()
    )

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found.",
        )

    return role


# ---------------------------------------------------------
# CREATE ROLE + USER
# ---------------------------------------------------------
#
# ADMIN only
#
# POST /api/roles/
#
# Example:
#
# {
#   "role": "FARM_MANAGER",
#   "description": "Manages farm operations",
#   "user_name": "John Manager",
#   "user_email": "john@example.com",
#   "user_password": "Manager@2026"
# }
#
# ---------------------------------------------------------

@router.post(
    "/",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Create a role and its first user account.
    """

    # -----------------------------------------------------
    # Check whether the role already exists.
    #
    # API field "role" maps to database column Role.name.
    # -----------------------------------------------------

    existing_role = (
        db.query(Role)
        .filter(Role.name == role_data.role)
        .first()
    )

    if existing_role is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A role with this name already exists.",
        )

    # -----------------------------------------------------
    # Check whether the email already exists.
    # -----------------------------------------------------

    existing_user = (
        db.query(User)
        .filter(User.email == role_data.user_email)
        .first()
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    # -----------------------------------------------------
    # Create the role.
    # -----------------------------------------------------

    role = Role(
        name=role_data.role,
        description=role_data.description,
        is_system=False,
    )

    db.add(role)

    # -----------------------------------------------------
    # Create the user account.
    #
    # The password is hashed before being stored.
    # -----------------------------------------------------

    user = User(
        name=role_data.user_name,
        email=role_data.user_email,
        password_hash=hash_password(
            role_data.user_password
        ),
        role=role_data.role,
    )

    db.add(user)

    # -----------------------------------------------------
    # Save both objects together.
    # -----------------------------------------------------

    try:

        db.commit()

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create role and user.",
        )

    # -----------------------------------------------------
    # Refresh the role so SQLAlchemy has the generated ID
    # and created_at values.
    # -----------------------------------------------------

    db.refresh(role)

    return role


# ---------------------------------------------------------
# UPDATE ROLE
# ---------------------------------------------------------
#
# ADMIN only
#
# PUT /api/roles/{role_id}
# ---------------------------------------------------------

@router.put(
    "/{role_id}",
    response_model=RoleResponse,
)
def update_role(
    role_id: uuid.UUID,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Update an existing role.
    """

    # -----------------------------------------------------
    # Find the role.
    # -----------------------------------------------------

    role = (
        db.query(Role)
        .filter(Role.id == role_id)
        .first()
    )

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found.",
        )

    # -----------------------------------------------------
    # Remember the old role name.
    #
    # Users currently store their role as a string.
    # If the role name changes, we also need to update
    # users assigned to the old role.
    # -----------------------------------------------------

    old_role_name = role.name

    # -----------------------------------------------------
    # Update role name.
    # -----------------------------------------------------

    if role_data.role is not None:

        existing_role = (
            db.query(Role)
            .filter(
                Role.name == role_data.role,
                Role.id != role_id,
            )
            .first()
        )

        if existing_role is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A role with this name already exists.",
            )

        role.name = role_data.role

    # -----------------------------------------------------
    # Update description.
    # -----------------------------------------------------

    if role_data.description is not None:
        role.description = role_data.description

    # -----------------------------------------------------
    # If the role name changed, update users that belong
    # to the old role.
    # -----------------------------------------------------

    if (
        role_data.role is not None
        and role_data.role != old_role_name
    ):

        users = (
            db.query(User)
            .filter(User.role == old_role_name)
            .all()
        )

        for user in users:
            user.role = role_data.role

    # -----------------------------------------------------
    # Save changes.
    # -----------------------------------------------------

    db.commit()
    db.refresh(role)

    return role


# ---------------------------------------------------------
# DELETE ROLE
# ---------------------------------------------------------
#
# ADMIN only
#
# DELETE /api/roles/{role_id}
# ---------------------------------------------------------

@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_role(
    role_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Delete an existing role.
    """

    # -----------------------------------------------------
    # Find the role.
    # -----------------------------------------------------

    role = (
        db.query(Role)
        .filter(Role.id == role_id)
        .first()
    )

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found.",
        )

    # -----------------------------------------------------
    # Check whether users are still using this role.
    #
    # We do not want to leave users with a role that
    # no longer exists.
    # -----------------------------------------------------

    users_with_role = (
        db.query(User)
        .filter(User.role == role.name)
        .count()
    )

    if users_with_role > 0:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "This role cannot be deleted because "
                "users are still assigned to it."
            ),
        )

    # -----------------------------------------------------
    # Delete the role.
    # -----------------------------------------------------

    db.delete(role)

    db.commit()

    return None