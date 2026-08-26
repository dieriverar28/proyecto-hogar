FROM python:3.13-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#--FROM python:3.13-slim → imagen base liviana con Python 
#(equivalente a tu FROM eclipse-temurin:21-jdk que probablemente usas en EcoMarketV, pero para Python)
#--WORKDIR /code → carpeta de trabajo dentro del contenedor
#--COPY requirements.txt . + RUN pip install → se copian las dependencias primero 
#y se instalan antes de copiar el resto del código. Esto es una optimización de cache de Docker: 
#si solo cambias tu código (no las dependencias), Docker reutiliza la capa ya 
#construida de pip install en vez de reinstalar todo de nuevo — acelera muchísimo los rebuilds
#--host 0.0.0.0 → crítico: por defecto, uvicorn escucha solo en 127.0.0.1 (localhost),
#lo que significa que solo aceptaría conexiones desde dentro del propio contenedor. 
#Con 0.0.0.0 escucha en todas las interfaces, permitiendo que el tráfico llegue desde 
#fuera del contenedor (vía el mapeo de puertos de Docker).
#Nota que no hay --reload aquí — eso es solo para desarrollo; en el contenedor "de producción" 
#no queremos que se reinicie solo ni que use el modo de recarga en caliente