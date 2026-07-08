from fastapi import APIRouter, Request, Header, HTTPException
from app.permissions import validate_permission
from app.core.security import resolve_context

router = APIRouter()

@router.get("/secure-test")
def secure_test(
    request: Request,
    x_app_id: int | None = Header(None),
    x_client_id: int | None = Header(None),
    authorization: str | None = Header(None),
):
    app_id, client_id = resolve_context(request, x_app_id, x_client_id)

    if not app_id or not client_id:
        raise HTTPException(status_code=400, detail="Missing context")

    validate_permission(
        request=request,
        username="system",
        app_id=app_id,
        client_id=client_id,
        authorization=authorization,
    )

    return {"status": "authorized"}