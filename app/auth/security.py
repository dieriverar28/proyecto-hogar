#hasheo de contraseñas y creación/verificación de tokens JWT

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None

"""
-pwd_context → usa bcrypt (el mismo algoritmo que BCryptPasswordEncoder 
de Spring Security), configurado una sola vez.
-hash_password / verify_password → funciones simples para hashear al registrar y verificar al hacer login. 
Equivalente directo a lo que ya conocemos.
-create_access_token → arma el JWT. El data típicamente va a ser algo como {"sub": usuario.email} 
(el "subject" del token — quién es el dueño). 
Le agregamos automáticamente la fecha de expiración (exp), usando el tiempo definido en config.py.
-decode_access_token → verifica que el token sea válido (firma correcta, no expirado) 
y devuelve su contenido, o None si es inválido.
"""