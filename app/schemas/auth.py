# Pydantic base class used for API request and response schemas.
from pydantic import BaseModel, EmailStr


# ---------------------------------------------------------
# Login request
# ---------------------------------------------------------
# Data the user sends when logging in.
class LoginRequest(BaseModel):

    # User's email address.
    email: EmailStr

    # User's plain-text password.
    password: str


# ---------------------------------------------------------
# Login response
# ---------------------------------------------------------
# Data returned after successful authentication.
class LoginResponse(BaseModel):

    # JWT access token.
    access_token: str

    # Token type used by the Authorization header.
    token_type: str = "bearer"

    # Basic information about the authenticated user.
    user_id: str
    name: str
    email: EmailStr

# ---------------------------------------------------------
# CHANGE PASSWORD REQUEST
# ---------------------------------------------------------
#
# Schema used when an authenticated user wants to change
# their password.
#
# The user must provide:
#
#   - Their current password
#   - Their new password
#   - Confirmation of the new password
#
# The current password is verified before the new password
# is saved.
#
# The authenticated user's identity comes from the JWT token,
# so the user does not need to provide their user ID or email.
#
# ---------------------------------------------------------

class ChangePasswordRequest(BaseModel):

    # -----------------------------------------------------
    # Current password
    # -----------------------------------------------------
    #
    # The password the user is currently using.
    #
    current_password: str

    # -----------------------------------------------------
    # New password
    # -----------------------------------------------------
    #
    # The password the user wants to use from now on.
    #
    new_password: str

    # -----------------------------------------------------
    # Confirm new password
    # -----------------------------------------------------
    #
    # Must match the new password.
    #
    confirm_password: str


# ---------------------------------------------------------
# CHANGE PASSWORD RESPONSE
# ---------------------------------------------------------
#
# Response returned after the password has been changed
# successfully.
#
# ---------------------------------------------------------

class ChangePasswordResponse(BaseModel):

    # Message confirming the password was changed.

    message: str


# ---------------------------------------------------------
# FORGOT PASSWORD REQUEST
# ---------------------------------------------------------
#
# Used when a user has forgotten their password.
#
# The user provides their email address.
#
# ---------------------------------------------------------

class ForgotPasswordRequest(BaseModel):

    # Email address associated with the user's account.

    email: EmailStr


# ---------------------------------------------------------
# FORGOT PASSWORD RESPONSE
# ---------------------------------------------------------
#
# Generic response returned after requesting a password
# reset.
#
# We use a generic message so we do not reveal whether
# an email address exists in the system.
#
# ---------------------------------------------------------

class ForgotPasswordResponse(BaseModel):

    # Confirmation message.

    message: str


# ---------------------------------------------------------
# VERIFY RESET CODE REQUEST
# ---------------------------------------------------------
#
# Used to verify the one-time password reset code.
#
# ---------------------------------------------------------

class VerifyResetCodeRequest(BaseModel):

    # Email address associated with the reset request.

    email: EmailStr

    # One-time reset code.

    code: str


# ---------------------------------------------------------
# VERIFY RESET CODE RESPONSE
# ---------------------------------------------------------
#
# Response returned when the reset code is valid.
#
# ---------------------------------------------------------

class VerifyResetCodeResponse(BaseModel):

    # Confirmation message.

    message: str


# ---------------------------------------------------------
# RESET PASSWORD REQUEST
# ---------------------------------------------------------
#
# Used to create a new password after the reset code
# has been verified.
#
# ---------------------------------------------------------

class ResetPasswordRequest(BaseModel):

    # Email address associated with the account.

    email: EmailStr

    # One-time reset code.

    code: str

    # New password.

    new_password: str

    # Confirmation of the new password.

    confirm_password: str


# ---------------------------------------------------------
# RESET PASSWORD RESPONSE
# ---------------------------------------------------------
#
# Response returned after the password has been reset.
#
# ---------------------------------------------------------

class ResetPasswordResponse(BaseModel):

    # Confirmation message.

    message: str