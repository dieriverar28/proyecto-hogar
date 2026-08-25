from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str


class UsuarioResponse(BaseModel):
    id: int
    email: EmailStr
    nombre: str
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)