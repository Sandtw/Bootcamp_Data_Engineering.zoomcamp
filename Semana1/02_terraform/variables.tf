locals {
  data_lake_bucket = "dtc_data_lake"
}

variable "credentials" {
  type = string
  description = "Ruta al archivo de credenciales de Google Cloud Platform en formato JSON"
  default = "C:/SAND_ZOOMP/Classes/Semana1/02_terraform/root-blueprint-379706-58cd41798659.json"
}

variable "project" {
    description = "Your GCP Project ID"
    default = "root-blueprint-379706"
}

variable "region" {
  description = "Región para recursos de GCP. Elija según su ubicación: https://cloud.google.com/about/locations"
  default = "us-west1"
  type = string
}

variable "storage_class" {
    description = "Tipo de clase de almacenamiento para su bucket. Consulte los documentos oficiales para obtener más información."
    default = "STANDARD"
}

variable "BQ_DATASET" {
    description = "Conjunto de datos de BigQuery en el que se escribirán los datos sin procesar (de GCS)"
    type = string
    default = "trips_data_all"
}

variable "TABLE_NAME" {
    description = "BigQuery Table"
    type = string
    default = "ny_trips"
}