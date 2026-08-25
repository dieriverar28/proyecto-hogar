from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List

from app.database import get_db
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.ubicacion import Ubicacion
from app.models.usuario import Usuario
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/productos", tags=["productos"])


def _validar_relaciones(db: Session, categoria_id: int, ubicacion_id: int):
    if not db.query(Categoria).filter(Categoria.id == categoria_id).first():
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if not db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first():
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")


@router.get("/", response_model=List[ProductoResponse])
def listar_productos(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return db.query(Producto).all()


@router.get("/proximos-a-vencer", response_model=List[ProductoResponse])
def productos_proximos_a_vencer(
    dias: int = 7,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    limite = date.today() + timedelta(days=dias)
    return (
        db.query(Producto)
        .filter(Producto.fecha_vencimiento.isnot(None))
        .filter(Producto.fecha_vencimiento <= limite)
        .order_by(Producto.fecha_vencimiento.asc())
        .all()
    )


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(
    producto_data: ProductoCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    _validar_relaciones(db, producto_data.categoria_id, producto_data.ubicacion_id)

    nuevo_producto = Producto(**producto_data.model_dump())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto


@router.patch("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int,
    producto_data: ProductoUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    datos_actualizados = producto_data.model_dump(exclude_unset=True)

    if "categoria_id" in datos_actualizados or "ubicacion_id" in datos_actualizados:
        _validar_relaciones(
            db,
            datos_actualizados.get("categoria_id", producto.categoria_id),
            datos_actualizados.get("ubicacion_id", producto.ubicacion_id),
        )

    for campo, valor in datos_actualizados.items():
        setattr(producto, campo, valor)

    db.commit()
    db.refresh(producto)
    return producto


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto)
    db.commit()