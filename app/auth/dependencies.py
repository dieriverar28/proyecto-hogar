#la "dependencia" que protege endpoints, extrayendo el usuario actual desde el token

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.security import decode_access_token
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise credentials_exception

    return usuario


"""
-OAuth2PasswordBearer(tokenUrl="/auth/login") → le dice a FastAPI (y a la documentación automática de Swagger) 
dónde está el endpoint de login. No hace magia por sí solo, pero habilita el botón "Authorize" 
en la documentación interactiva (/docs) para probar la API fácilmente con tu token.
-get_current_user → esta función es una dependencia que vas a "inyectar" en cualquier endpoint que quieras proteger. 
FastAPI automáticamente:
1. Extrae el token del header Authorization: Bearer <token> de la petición
2. Lo decodifica y valida
3. Busca al usuario correspondiente en la base de datos
4. Si todo está bien, te entrega el objeto Usuario directamente en tu endpoint
5. Si algo falla (token inválido, expirado, usuario no existe), 
lanza automáticamente un 401 Unauthorized
"""