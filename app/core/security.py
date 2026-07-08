import os
import requests

from fastapi import HTTPException, Request

from app.core.config import (
    CONTROL_PLANE_BASE_URL,
    CONTROL_PLANE_TIMEOUT,
    DOMAIN_APP_ID,
)


def resolve_context(
    request: Request,
    x_app_id: int | None,
    x_client_id: int | None,
):
    app_id = x_app_id
    client_id = x_client_id
    
    if app_id != DOMAIN_APP_ID:
        raise HTTPException(
            status_code=403,
            detail="Invalid domain application context",
        )

    if app_id is None:
        q = request.query_params.get("app_id")
        if q and q.isdigit():
            app_id = int(q)

    if client_id is None:
        q = request.query_params.get("client_id")
        if q and q.isdigit():
            client_id = int(q)

    return app_id, client_id


def _extract_bearer_or_cookie(
    request: Request,
    authorization: str | None = None,
) -> str | None:

    token = None

    if authorization and authorization.startswith("Bearer "):
        token = authorization

    if not token:
        raw_cookie = request.cookies.get("jwt")
        if raw_cookie:
            token = f"Bearer {raw_cookie}"

    return token


def _call_control_plane(
    request: Request,
    endpoint: str,
    app_id: int,
    client_id: int,
    authorization: str | None = None,
) -> requests.Response:

    bearer = _extract_bearer_or_cookie(
        request,
        authorization,
    )

    if not bearer:
        raise HTTPException(
            status_code=401,
            detail="No token",
        )

    try:
        response = requests.get(
            f"{CONTROL_PLANE_BASE_URL}{endpoint}",
            headers={
                "Authorization": bearer,
                "X-App-Id": str(app_id),
                "X-Client-Id": str(client_id),
            },
            timeout=CONTROL_PLANE_TIMEOUT,
        )

        return response

    except requests.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Control Plane no disponible: {e}",
        )


def validate_service_context(
    request: Request,
    app_id: int,
    client_id: int,
    authorization: str | None = None,
):
    """
    Validación de comunicación segura entre componentes.

    No valida permisos de usuario.

    Responsabilidad:
    - JWT válido.
    - Contexto de aplicación.
    - Contexto de cliente.
    - Comunicación autorizada por Control Plane.
    """

    response = _call_control_plane(
        request=request,
        endpoint="/internal/service-context-check",
        app_id=app_id,
        client_id=client_id,
        authorization=authorization,
    )

    if response.status_code == 200:
        return True

    try:
        payload = response.json()

        if isinstance(payload, dict):
            detail = payload.get(
                "detail",
                "Comunicación no autorizada",
            )
        else:
            detail = "Comunicación no autorizada"

    except Exception:
        detail = "Comunicación no autorizada"

    raise HTTPException(
        status_code=response.status_code,
        detail=detail,
    )