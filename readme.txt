#Proyecto de sqlite con flask y postman para manejar una base de datos de estudiantes de la FIIS

Requisitos:
- Python
- postman
- python environment con pip install -r requirements.txt


## Para insertar datos usar la url http://localhost:5000/insertar y método POST
usar formato Json:
{
  "codigo": "20210048F",
  "nombre": "Diego",
  "apellido": "Martin",
  "promedio": 12.7
}


## Para mostrar datos usar la url http://localhost:5000/mostrar y método GET


## Para mostrar datos por codigo usar la url http://localhost:5000/mostrar_codigo y método POST
usar formato Json:
{
  "codigo": "20210048F"
}


##Para eliminar un estudiante, usar la url http://localhost:5000/eliminar y método POST
usar formato Json:
{
  "codigo": "20210048F"
}