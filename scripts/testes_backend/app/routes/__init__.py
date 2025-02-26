from fastapi import APIRouter
from .usuario import usuario_router


router = APIRouter()
router.include_router(usuario_router)
