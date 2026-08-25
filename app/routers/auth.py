from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.auth.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo_usuario = Usuario(
        email=usuario_data.email,
        nombre=usuario_data.nombre,
        hashed_password=hash_password(usuario_data.password),
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    if not usuario or not verify_password(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )

    access_token = create_access_token(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}


"""
-APIRouter(prefix="/auth", tags=["auth"]) → agrupa estos endpoints bajo /auth/... y los organiza
 bajo la etiqueta "auth" en la documentación Swagger.
-register → verifica que el email no exista, hashea la contraseña,
 guarda el usuario. db.refresh(nuevo_usuario) recarga el objeto desde la base de datos 
 para traer el id y creado_en generados automáticamente.
-login → usa OAuth2PasswordRequestForm, una clase especial de FastAPI que espera
 un formulario (no JSON) con campos username y password — es el estándar OAuth2, 
 por eso el campo se llama username aunque nosotros lo usemos como email. 
 Si las credenciales son correctas, genera y devuelve el JWT.
-db.commit() → aquí es donde controlas explícitamente la transacción 
(recuerda que en database.py puse autocommit=False). Sin este commit(), 
el registro no se guardaría de verdad.
"""