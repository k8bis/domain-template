from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Text,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db import Base


class SystemProvider(Base):

    __tablename__ = "system_providers"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    provider_code = Column(
        String(100),
        nullable=False,
        unique=True,
    )

    provider_name = Column(
        String(150),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    is_enabled = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    services = relationship(
        "SystemService",
        back_populates="provider",
    )