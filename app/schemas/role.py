# ---------------------------------------------------------
# Role Schemas
# ---------------------------------------------------------
#
# Schemas used for:
#   - Creating roles and their first user account
#   - Updating roles
#   - Returning role information
#
# ---------------------------------------------------------

import uuid

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

# ---------------------------------------------------------
# CREATE ROLE
# ---------------------------------------------------------
#
# When an ADMIN creates a role, they also create the
# first user account that will use that role.
#
# ---------------------------------------------------------

class RoleCreate(BaseModel):

    # -----------------------------------------------------
    # Role information
    # -----------------------------------------------------

    role: str

    description: str | None = None

    # -----------------------------------------------------
    # First user account for this role
    # -----------------------------------------------------

    user_name: str

    user_email: EmailStr

    user_password: str


# ---------------------------------------------------------
# UPDATE ROLE
# ---------------------------------------------------------

class RoleUpdate(BaseModel):

    # New role name.
    role: str | None = None

    # New role description.
    description: str | None = None


# ---------------------------------------------------------*
# RESPONSE ROLE
# ---------------------------------------------------------*

class RoleResponse(BaseModel):

    # Unique role identifier.
    id: uuid.UUID

    # Role name returned by the API as "role".
    # The database column remains "name".
    role: str = Field(
        validation_alias="name",
        serialization_alias="role",
    )

    # Role description.
    description: str | None

    # System-defined role or custom role.
    is_system: bool

    # Date and time the role was created.
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )