from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/")
def root():
    return {
        "app": "rodel-pytemplate",
        "status": "ok"
    }