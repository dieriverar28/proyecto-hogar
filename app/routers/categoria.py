#CRUD más simple, para ver el patrón completo

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return db.query(Categoria).all()


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(
    categoria_data: CategoriaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    existente = db.query(Categoria).filter(Categoria.nombre == categoria_data.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    nueva_categoria = Categoria(nombre=categoria_data.nombre)
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(categoria)
    db.commit()

"""
-Cada endpoint tiene usuario_actual: Usuario = Depends(get_current_user) — esto los protege 
automáticamente, exigiendo un JWT válido.
-response_model=List[CategoriaResponse] → le dice a FastAPI que la respuesta es una
 lista de ese schema; se encarga de convertir y validar automáticamente.
-El patrón CRUD es directo: db.query(...), db.add(...), db.commit(), db.delete(...)
 — muy similar a usar un Repository de Spring Data JPA, 
 pero escrito explícitamente en el propio endpoint en vez de una interfaz separada 
 (para proyectos más grandes, normalmente se movería esta lógica a una capa de "servicio" aparte
"""