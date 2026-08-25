#Este archivo es el equivalente a tu clase @SpringBootApplication con el método main() 
# — arranca la aplicación y registra los routers.

from fastapi import FastAPI

from app.routers import auth, categoria, ubicacion, producto



app = FastAPI(
    title="Inventario Hogar API",
    description="API para gestionar el inventario doméstico",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(categoria.router)
app.include_router(ubicacion.router)
app.include_router(producto.router)

@app.get("/")
def root():
    return {"mensaje": "Inventario Hogar API funcionando"}

"""
-FastAPI(...) → crea la instancia de la app. Los parámetros title, description, 
version aparecen automáticamente en la documentación Swagger.
-app.include_router(...) → registra cada router que armamos, con sus prefijos
 (/auth, /categorias) ya incluidos.
-@app.get("/") → un endpoint simple de "health check" 
para verificar rápidamente que la API está viva.
"""