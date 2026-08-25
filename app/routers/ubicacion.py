from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.ubicacion import Ubicacion
from app.models.usuario import Usuario
from app.schemas.ubicacion import UbicacionCreate, UbicacionResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/ubicaciones", tags=["ubicaciones"])


@router.get("/", response_model=List[UbicacionResponse])
def listar_ubicaciones(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return db.query(Ubicacion).all()


@router.post("/", response_model=UbicacionResponse, status_code=status.HTTP_201_CREATED)
def crear_ubicacion(
    ubicacion_data: UbicacionCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    existente = db.query(Ubicacion).filter(Ubicacion.nombre == ubicacion_data.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="La ubicación ya existe")

    nueva_ubicacion = Ubicacion(nombre=ubicacion_data.nombre)
    db.add(nueva_ubicacion)
    db.commit()
    db.refresh(nueva_ubicacion)
    return nueva_ubicacion


@router.delete("/{ubicacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ubicacion(
    ubicacion_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    ubicacion = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    db.delete(ubicacion)
    db.commit()