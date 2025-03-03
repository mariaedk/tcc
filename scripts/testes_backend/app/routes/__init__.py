from fastapi import APIRouter
from .usuario import usuario_router
from .dispositivo import dispositivo_router
from .unidade_medida import unidade_router

router = APIRouter()
router.include_router(usuario_router)
router.include_router(dispositivo_router)
router.include_router(unidade_router)
