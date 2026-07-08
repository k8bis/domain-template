import os

from fastapi import APIRouter, Depends, Header, Request, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import (
    resolve_context,
    validate_service_context,
)
from app.models import SystemProvider

RODELSOFT_APP = os.getenv("RODELSOFT_APP")

router = APIRouter(
    prefix="/system",
    tags=["system"],
)


@router.get("/services")
def get_system_services(
    request: Request,
    db: Session = Depends(get_db),
    authorization: str | None = Header(default=None),
    x_app_id: int | None = Header(default=None),
    x_client_id: int | None = Header(default=None),
):

    app_id, client_id = resolve_context(
        request,
        x_app_id,
        x_client_id,
    )

    if not app_id or not client_id:
        raise HTTPException(
            status_code=400,
            detail="Missing context",
        )

    validate_service_context(
        request=request,
        app_id=app_id,
        client_id=client_id,
        authorization=authorization,
    )

    providers = (
        db.query(SystemProvider)
        .filter(
            SystemProvider.is_enabled.is_(True)
        )
        .order_by(
            SystemProvider.provider_name
        )
        .all()
    )

    result = []

    for provider in providers:

        services = []

        for service in provider.services:

            if service.is_enabled:
                services.append(
                    {
                        "service_code": service.service_code,
                        "service_name": service.service_name,
                        "description": service.description,
                        "enabled": service.is_enabled,
                    }
                )

        result.append(
            {
                "provider_code": provider.provider_code,
                "provider_name": provider.provider_name,
                "services": services,
            }
        )

    return {
        "domain": RODELSOFT_APP,
        "providers": result,
    }