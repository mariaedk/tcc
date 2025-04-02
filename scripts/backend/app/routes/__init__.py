from fastapi import APIRouter
from .usuario import usuario_router
from .dispositivo import dispositivo_router
from .unidade_medida import unidade_router
from .sensor import sensor_router
from .medicao import medicao_router
from .auth_rote import auth_router

router = APIRouter()
router.include_router(usuario_router)
router.include_router(dispositivo_router)
router.include_router(unidade_router)
router.include_router(sensor_router)
router.include_router(medicao_router)
router.include_router(auth_router)