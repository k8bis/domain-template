from fastapi import HTTPException, Request

from app.core.security import (
    _call_control_plane,
)


def validate_permission(
    request: Request,
    username: str,
    app_id: int,
    client_id: int,
    authorization: str | None = None,
):
    response = _call_control_plane(
        request=request,
        endpoint="/internal/access-check",
        app_id=app_id,
        client_id=client_id,
        authorization=authorization,
    )

    if response.status_code == 200:
        return True

    detail = _extract_error_detail(
        response,
        "Acceso denegado por Control Plane",
    )

    raise HTTPException(
        status_code=response.status_code,
        detail=detail,
    )


def _extract_error_detail(
    response,
    fallback: str,
) -> str:

    try:
        payload = response.json()

        if isinstance(payload, dict):
            return payload.get(
                "detail",
                fallback,
            )

        return fallback

    except Exception:
        return fallback


def get_context_info(
    request: Request,
    app_id: int,
    client_id: int,
    authorization: str | None = None,
) -> dict:

    response = _call_control_plane(
        request=request,
        endpoint="/internal/context-info",
        app_id=app_id,
        client_id=client_id,
        authorization=authorization,
    )

    if response.status_code == 200:
        payload = response.json()

        return (
            payload
            if isinstance(payload, dict)
            else {}
        )

    detail = _extract_error_detail(
        response,
        "No se pudo obtener contexto desde Control Plane",
    )

    raise HTTPException(
        status_code=response.status_code,
        detail=detail,
    )


def get_session_context(
    request: Request,
    app_id: int,
    client_id: int,
    authorization: str | None = None,
) -> dict:

    response = _call_control_plane(
        request=request,
        endpoint="/public/session-context",
        app_id=app_id,
        client_id=client_id,
        authorization=authorization,
    )

    if response.status_code == 200:
        payload = response.json()

        return (
            payload
            if isinstance(payload, dict)
            else {}
        )

    detail = _extract_error_detail(
        response,
        "No se pudo obtener session-context desde Control Plane",
    )

    raise HTTPException(
        status_code=response.status_code,
        detail=detail,
    )


def get_role_info(
    request: Request,
    app_id: int,
    client_id: int,
    authorization: str | None = None,
) -> dict:

    session = get_session_context(
        request=request,
        app_id=app_id,
        client_id=client_id,
        authorization=authorization,
    )

    role = str(
        session.get("role") or "member"
    ).strip().lower()

    is_system_admin = (
        bool(session.get("is_system_admin", False))
        or role == "system_admin"
    )

    is_app_client_admin = (
        bool(session.get("is_app_client_admin", False))
        or role == "app_client_admin"
    )

    is_member = (
        bool(session.get("is_member", False))
        or (
            not is_system_admin
            and not is_app_client_admin
        )
    )

    return {
        "role": role,
        "is_system_admin": is_system_admin,
        "is_app_client_admin": is_app_client_admin,
        "is_member": is_member,

        "can_manage_catalogs":
            is_system_admin or is_app_client_admin,

        "can_view_pos_config":
            is_system_admin or is_app_client_admin,

        "can_edit_pos_config":
            is_system_admin,
    }