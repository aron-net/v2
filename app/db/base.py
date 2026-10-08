"""
BPU Nexus - Database Model Base

Purpose:
    Defines the common SQLAlchemy base class that all
    BPU Nexus database models will inherit from.

Used by:
    Database models such as User, ProcurementRecord,
    AuditLog, and other future database tables.

Why we need it:
    SQLAlchemy needs a common registry that keeps track
    of all our database models.

If changing later:
    Database models should inherit from Base.
    Do not create separate declarative bases for individual
    models unless there is a specific architectural reason.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all BPU Nexus SQLAlchemy models.

    Every database model we create later will inherit from
    this class.

    Example:

        class User(Base):
            ...

    SQLAlchemy will then know that User represents a
    database table.
    """

    pass