# Podemos especificar todas las instrucciones que queremos ejecutar para crear una nueva imagen
# basada en lo que queramos 
FROM python:3.9.1

RUN apt-get install wget
#? Instalara pandas dentro del contenedor y creara una nueva imagen basada en eso
RUN pip install pandas sqlalchemy psycopg2
#? Ubicacion en la imagen en el contenedor donde copiaremos el archivo
WORKDIR /app
#? Nombre en nuestra "maquina host" "nombre en el destino"
COPY ingest_data.py ingest_data.py

#! Cuando ejecute docker, quiero que haga python ingest_data.py
ENTRYPOINT ["python", "ingest_data.py"]