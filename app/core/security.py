"""
BPU Nexus - Security Utilities

Purpose:
    Central location for password hashing
    and JWT token generation.

Used by:
    Authentication endpoints such as
    register and login.

Security:
    Plain text passwords are NEVER stored
    in PostgreSQL.

    Passwords are hashed using bcrypt.

    JWT tokens are signed using the
    configured secret key.
"""

from datetime import datetime, timedelta, UTC

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


# ---------------------------------------------------------
# PASSWORD HASHING
# ---------------------------------------------------------

# CryptContext manages password hashing algorithms.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Convert a plain text password into a
    secure bcrypt hash.
    """

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify whether a plain text password
    matches a stored hash.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ---------------------------------------------------------
# JWT ACCESS TOKENS
# ---------------------------------------------------------

def create_access_token(
    subject: str,
) -> str:
    """
    Create a JWT access token.

    subject:
        Usually the user's database ID.
    """

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    return token
