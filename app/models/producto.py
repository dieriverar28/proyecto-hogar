#modelo principal de la tabla productos con relaciones

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    cantidad = Column(Float, nullable=False, default=0)
    unidad = Column(String, nullable=False)  # ej: "kg", "unidades", "litros"
    fecha_vencimiento = Column(Date, nullable=True)
    fecha_ingreso = Column(Date, nullable=False)

    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    ubicacion_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=False)

    categoria = relationship("Categoria")
    ubicacion = relationship("Ubicacion")

"""
-Column(...) reemplaza las anotaciones @Column. Los tipos (Integer, String, Float, Date) 
son clases de SQLAlchemy, no tipos nativos de Python.
-ForeignKey("categorias.id") reemplaza tu @ManyToOne @JoinColumn — aquí se referencia como texto 
"tabla.columna" en vez de la clase Java directamente. 
Esto evita problemas de referencias circulares entre archivos.
-relationship(...) es lo que te permite acceder a producto.categoria.nombre directamente en Python 
(carga el objeto relacionado), similar a cómo funciona @ManyToOne en JPA — pero aquí es explícito: la Column con ForeignKey guarda el ID en la tabla,
y relationship es una capa extra que carga el objeto completo cuando lo necesitas.
-No hay @Entity — heredar de Base ya es suficiente para que SQLAlchemy sepa que es una tabla.
-__tablename__ es obligatorio y explícito (en JPA a veces se infiere del nombre de la clase; aquí siempre lo defines tú).
"""