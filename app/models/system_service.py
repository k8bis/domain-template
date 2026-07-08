from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Text,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db import Base


class SystemService(Base):

    __tablename__ = "system_services"

    __table_args__ = (
        UniqueConstraint(
            "provider_id",
            "service_code",
            name="uq_system_services_provider_service",
        ),
    )

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    provider_id = Column(
        BigInteger,
        ForeignKey(
            "system_providers.id"
        ),
        nullable=False,
    )

    service_code = Column(
        String(100),
        nullable=False,
    )

    service_name = Column(
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

    provider = relationship(
        "SystemProvider",
        back_populates="services",
    )