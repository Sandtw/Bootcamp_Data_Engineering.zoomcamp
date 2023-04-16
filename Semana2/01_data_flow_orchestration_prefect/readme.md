## Pasos de construcción de un pipeline con PREFECT

Carpetas iniciales

01_DATA_FLOW_ORCHESTATION_PREFECT/
├── data/
│   ├── yellow/
├── flows/
│   ├── 01_start/
│   ├── 02_gcp/
│   │   ├── etl_web_to_gcs.py
├── requirements.txt


Ruta de los csv de yellow taxi
https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow

Esta forma de definir rutas de archivo es más legible y menos propensa a errores que simplemente usar una cadena de texto. 
path = Path(f"data/{color}/{dataset_file}.parquet")

De esta manera cargamos el cloud storage
gcs_block = GcsBucket.load("zoomp-gcs")

Y podemos cargar datos directamente a cloud storage mediante una url en nuestro entirno local de archivo (si no contiene carpetas en el bucket los crea)
gcs_block.upload_from_path(from_path=path, to_path=path)

Instalamos pyarrow, porque necesitamos un motor adecuado para manejar la escritura de datos en formato parquet
conda install pyarrow


Si el archivo que llama se encuentra en la carpeta raiz la ruta data/yellow/dataset_file.parquet funcionará. Si el archivo que llama se encuentra en una ubicación diferente, entonces se necesitará una ruta relativa 
path = Path(f"../../data/{color}/{dataset_file}.parquet")

Documentacion de prefect_gcp: https://prefecthq.github.io/prefect-gcp/cloud_storage/

