from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

from app.schemas.categoria import CategoriaResponse
from app.schemas.ubicacion import UbicacionResponse


class ProductoCreate(BaseModel):
    nombre: str
    cantidad: float
    unidad: str
    fecha_vencimiento: Optional[date] = None
    fecha_ingreso: date
    categoria_id: int
    ubicacion_id: int


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    cantidad: Optional[float] = None
    unidad: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    categoria_id: Optional[int] = None
    ubicacion_id: Optional[int] = None


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    cantidad: float
    unidad: str
    fecha_vencimiento: Optional[date]
    fecha_ingreso: date
    categoria: CategoriaResponse
    ubicacion: UbicacionResponse

    model_config = ConfigDict(from_attributes=True)

"""
-ProductoCreate recibe categoria_id y ubicacion_id como enteros simples 
(el cliente solo manda el ID)
-ProductoUpdate tiene todos los campos opcionales (Optional[...] = None) — esto permite actualizaciones parciales (PATCH),
 donde el cliente solo envía los campos que quiere cambiar
-ProductoResponse en cambio devuelve categoria y ubicacion como objetos completos anidados 
(CategoriaResponse, UbicacionResponse), no solo el ID — así el cliente recibe el nombre de la categoría/ubicación
 sin tener que hacer otra consulta. Esto funciona automáticamente gracias a las relationship() 
 que definimos en el modelo Producto, combinado con from_attributes=True.
"""