from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from database import get_db
import models
from security import verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


class LoginAgent(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
def login_json(payload: LoginAgent, db: Session = Depends(get_db)):
    agent = (
        db.query(models.Agent)
        .filter(models.Agent.email == payload.email)
        .first()
    )
    # <--- IMPORTANT: vérifier agent avant d'accéder à agent.password
    if agent is None or not verify_password(payload.password, agent.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )

    access_token = create_access_token(data={"sub": agent.id})
    return {"access_token": access_token, "token_type": "bearer"}
