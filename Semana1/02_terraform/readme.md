## Pasos de ejecución de infraestructura mediane Terraform:

> Paso 1: Enlazar consola con GCP 

Cualquier consola de comandos acepta este proceso

```python
    gcloud auth login
    gcloud projects list    # Lista los ID de proyectos contenidos
    gcloud config set project [id_project]
```

> Paso 2: Enlazando la cuenta de servicio mediante la key.json y ejecución de terrraform.

***Usando*** la opcion sin Variable `credentials` y sin establecer el *id* de proyecto

```c#
  provider "google" {
  project = var.project
  region = var.region
}
```

```c#
variable "project" {
    description = "Your GCP Project ID"
#   default = "id_project"
}
```

En windows: 

```python
    set GOOGLE_APPLICATION_CREDENTIALS=.../key.json # La ruta va sin comillas
    terraform init
    terraform plan
```

Pide que ingreses el *ID_PROJECT*

```bash
var.project
  Your GCP Project ID

  Enter a value: id_project
```

y luego puedes aplicar el plan mostrado

```python
    terraform apply
```

En el caso de no querer establecer variable de entorno **GOOGLE_APPLICATION_CREDENTIALS**, podemos definirlo mediante variables

```c#
# En archivo variables.tf
variable "credentials" {
  type = string
  description = "archivo en formato JSON"
  default = ".../.../key.json"
}
```
```c#
# En archivo main.tf
provider "google" {
  project = var.project
  region = var.region
  credentials = file(var.credentials) 
}
```

```python
    terraform init
    terraform plan
    tarraform apply
```

Cuya recursos definidos se visualizan en GCP, tanto en *Cloud storage* y *Bigquery*

> Paso 3: Eliminar recursos definidos en el proveedor de nube


```python
    terraform destroy
```