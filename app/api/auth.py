# Used to work with UUID values.
import uuid
import secrets
from datetime import datetime, timedelta

# FastAPI tools for creating the API route and handling errors.
from fastapi import APIRouter, Depends, HTTPException, status

# SQLAlchemy database session.
from sqlalchemy.orm import Session

# Database dependency.
from app.db.dependencies import get_db

# User database model.
from app.models.user import User

# Password reset token database model.
from app.models.password_reset_token import PasswordResetToken

# Authentication helpers.
from app.core.security import (
    verify_password,
    create_access_token,
    hash_password,
)

# Login request and response schemas.
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    VerifyResetCodeRequest,
    VerifyResetCodeResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
)


# ---------------------------------------------------------
# Authentication router
# ---------------------------------------------------------
router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------
@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    # Find the user using the email address.
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    # Do not reveal whether the email exists.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    # Verify the password against the stored bcrypt hash.
    password_is_valid = verify_password(
        data.password,
        user.password_hash,
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    # Convert the user's UUID to a string for the JWT subject.
    access_token = create_access_token(
        subject=str(user.id),
    )

    # Return the access token and basic user information.
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user.id),
        name=user.name,
        email=user.email,
    )

# ---------------------------------------------------------
# Current authenticated user dependency.
# ---------------------------------------------------------

from app.api.dependencies import get_current_user

# ---------------------------------------------------------
# Change password
# ---------------------------------------------------------
#
# Allows an authenticated user to change their password.
#
# The user must provide:
#   - Current password
#   - New password
#   - Confirmation of the new password
#
# The user's identity comes from the JWT token.
#
# ---------------------------------------------------------

@router.post(
    "/change-password",
    response_model=ChangePasswordResponse,
)
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # -----------------------------------------------------
    # Verify the current password.
    # -----------------------------------------------------

    password_is_valid = verify_password(
        data.current_password,
        current_user.password_hash,
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    # -----------------------------------------------------
    # Make sure the new password and confirmation match.
    # -----------------------------------------------------

    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirmation do not match.",
        )

    # -----------------------------------------------------
    # Prevent using the same password again.
    # -----------------------------------------------------

    if data.current_password == data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from the current password.",
        )

    # -----------------------------------------------------
    # Hash the new password.
    # -----------------------------------------------------

    current_user.password_hash = hash_password(
        data.new_password,
    )

    # -----------------------------------------------------
    # Save the new password.
    # -----------------------------------------------------

    db.commit()

    # -----------------------------------------------------
    # Return success response.
    # -----------------------------------------------------

    return ChangePasswordResponse(
        message="Password changed successfully.",
    )

# ---------------------------------------------------------
# Forgot password
# ---------------------------------------------------------
#
# Starts the password-reset process.
#
# The user provides their email address.
#
# If the account exists:
#   1. Generate a secure one-time code.
#   2. Hash the code.
#   3. Store the hash in the database.
#   4. Give the code a short expiration time.
#
# In production, the code will be sent by email.
#
# For development, we will temporarily print the code
# in the backend terminal so we can test the complete flow.
#
# ---------------------------------------------------------

@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
)
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):

    # -----------------------------------------------------
    # Find the user by email.
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    # -----------------------------------------------------
    # Always return the same response.
    #
    # This prevents revealing whether an email exists.
    # -----------------------------------------------------

    generic_message = (
        "If an account exists for this email, "
        "a password reset code has been generated."
    )

    if not user:
        return ForgotPasswordResponse(
            message=generic_message,
        )

    # -----------------------------------------------------
    # Invalidate previous unused reset codes.
    # -----------------------------------------------------

    existing_tokens = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        )
        .all()
    )

    for token in existing_tokens:
        token.used_at = datetime.utcnow()

    # -----------------------------------------------------
    # Generate a secure six-digit reset code.
    # -----------------------------------------------------

    reset_code = f"{secrets.randbelow(1_000_000):06d}"

    # -----------------------------------------------------
    # Hash the reset code before storing it.
    # -----------------------------------------------------

    code_hash = hash_password(reset_code)

    # -----------------------------------------------------
    # Create a new reset-token record.
    #
    # The code will expire after 10 minutes.
    # -----------------------------------------------------

    reset_token = PasswordResetToken(
        user_id=user.id,
        code_hash=code_hash,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
    )

    db.add(reset_token)
    db.commit()

    # -----------------------------------------------------
    # DEVELOPMENT ONLY
    # -----------------------------------------------------
    #
    # We do not have an email service connected yet.
    #
    # Therefore, print the code in the backend terminal
    # so we can test the reset flow.
    #
    # DO NOT use this approach in production.
    # -----------------------------------------------------

    print(
        f"[DEV] Password reset code for {user.email}: "
        f"{reset_code}"
    )

    return ForgotPasswordResponse(
        message=generic_message,
    )

# ---------------------------------------------------------
# Verify password reset code
# ---------------------------------------------------------
#
# Checks the most recent unused reset code for the user.
#
# The code must:
#   1. Exist
#   2. Not have been used
#   3. Not be expired
#   4. Match the stored bcrypt hash
#
# ---------------------------------------------------------

@router.post(
    "/verify-reset-code",
    response_model=VerifyResetCodeResponse,
)
def verify_reset_code(
    data: VerifyResetCodeRequest,
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # Find the most recent unused reset token
    # for this user's email.
    # -----------------------------------------------------

    token = (
        db.query(PasswordResetToken)
        .join(
            User,
            PasswordResetToken.user_id == User.id,
        )
        .filter(
            User.email == data.email,
            PasswordResetToken.used_at.is_(None),
        )
        .order_by(
            PasswordResetToken.created_at.desc()
        )
        .first()
    )

    # -----------------------------------------------------
    # No valid reset token was found.
    # -----------------------------------------------------

    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset code.",
        )

    # -----------------------------------------------------
    # Check whether the reset code has expired.
    # -----------------------------------------------------

    if token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset code.",
        )

    # -----------------------------------------------------
    # Compare the supplied code with the stored
    # bcrypt hash.
    # -----------------------------------------------------

    code_is_valid = verify_password(
        data.code,
        token.code_hash,
    )

    if not code_is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset code.",
        )

    # -----------------------------------------------------
    # Code is valid.
    # -----------------------------------------------------

    return VerifyResetCodeResponse(
        message="Reset code verified successfully.",
    )

# ---------------------------------------------------------
# Reset password
# ---------------------------------------------------------
#
# Allows a user to set a new password using a valid
# password-reset code.
#
# The reset code must:
#   1. Exist
#   2. Belong to the supplied email
#   3. Not have been used
#   4. Not be expired
#   5. Match the stored bcrypt hash
#
# The code is marked as used only after the password
# has been successfully changed.
#
# ---------------------------------------------------------

@router.post(
    "/reset-password",
    response_model=ResetPasswordResponse,
)
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # Find the most recent unused reset token.
    # -----------------------------------------------------

    token = (
        db.query(PasswordResetToken)
        .join(
            User,
            PasswordResetToken.user_id == User.id,
        )
        .filter(
            User.email == data.email,
            PasswordResetToken.used_at.is_(None),
        )
        .order_by(
            PasswordResetToken.created_at.desc()
        )
        .first()
    )

    # -----------------------------------------------------
    # Make sure a reset token exists.
    # -----------------------------------------------------

    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset code.",
        )

    # -----------------------------------------------------
    # Make sure the code has not expired.
    # -----------------------------------------------------

    if token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset code.",
        )

    # -----------------------------------------------------
    # Verify the reset code.
    # -----------------------------------------------------

    code_is_valid = verify_password(
        data.code,
        token.code_hash,
    )

    if not code_is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset code.",
        )

    # -----------------------------------------------------
    # Make sure the new password and confirmation match.
    # -----------------------------------------------------

    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirmation do not match.",
        )

    # -----------------------------------------------------
    # Find the user associated with the reset token.
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(User.id == token.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to reset password.",
        )

    # -----------------------------------------------------
    # Hash and save the new password.
    # -----------------------------------------------------

    user.password_hash = hash_password(
        data.new_password,
    )

    # -----------------------------------------------------
    # Mark the reset token as used.
    #
    # This prevents the same code from being reused.
    # -----------------------------------------------------

    token.used_at = datetime.utcnow()

    # -----------------------------------------------------
    # Save everything in one database transaction.
    # -----------------------------------------------------

    db.commit()

    # -----------------------------------------------------
    # Return success response.
    # -----------------------------------------------------

    return ResetPasswordResponse(
        message="Password reset successfully.",
    )