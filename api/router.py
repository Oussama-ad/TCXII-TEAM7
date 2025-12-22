from fastapi import APIRouter
from api.endpoints import agents, auth, callsession

api_router = APIRouter()
api_router.include_router(agents.router)
api_router.include_router(auth.router)
api_router.include_router(callsession.router)
