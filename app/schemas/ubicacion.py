from pydantic import BaseModel, ConfigDict


class UbicacionCreate(BaseModel):
    nombre: str


class UbicacionResponse(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)