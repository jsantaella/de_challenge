# LATAM Data Engineering Challenge

En el presente repositorio se encontrarán las soluciones los requerimientos planteados por el ejercicio. 
Los resultados esperados fueron los siguientes para cada uno de los ejercicios: 

- Fechas con mayor cantidad de trinos y usuario que más trinó respectivamente
    - [(datetime.date(2021, 2, 12), 'RanbirS00614606'), (datetime.date(2021, 2, 13), 'MaanDee08215437'), (datetime.date(2021, 2, 17), 'RaaJVinderkaur'), (datetime.date(2021, 2, 16), 'jot__b'), (datetime.date(2021, 2, 14), 'rebelpacifist'), (datetime.date(2021, 2, 18), 'neetuanjle_nitu'), (datetime.date(2021, 2, 15), 'jot__b'), (datetime.date(2021, 2, 20), 'MangalJ23056160'), (datetime.date(2021, 2, 23), 'Surrypuria'), (datetime.date(2021, 2, 19), 'Preetm91'), (datetime.date(2021, 2, 21), 'Surrypuria'), (datetime.date(2021, 2, 22), 'preetysaini321'), (datetime.date(2021, 2, 24), 'preetysaini321')]

- Conteo de emojis: 
    -[('🙏', 7286), ('😂', 3072), ('🚜', 2972), ('✊', 2411), ('🌾', 2182), ('🇮', 2092), ('❤', 1779), ('🤣', 1668), ('👇', 1108), ('💚', 1040)]

- Top usuarios mencionados en el lote de trinos: 
    -[('narendramodi', 2265), ('Kisanektamorcha', 1840), ('RakeshTikaitBKU', 1644), ('PMOIndia', 1427), ('RahulGandhi', 1146), ('GretaThunberg', 1048), ('RaviSinghKA', 1019)]

## Estructura del repositorio

El arbol de archivos del repositorio es el siguiente: 
```
├───pyspark_scripts
│   └───code
├───src
└───terraform
    └───.terraform
        ├───modules
        │   ├───bucket
        │   │   ├───.github
        │   │   │   └───workflows
        │   │   ├───build
        │   │   ├───docs
        │   │   ├───examples
        │   │   │   ├───multiple_buckets
        │   │   │   └───simple_bucket
        │   │   ├───helpers
        │   │   ├───modules
        │   │   │   └───simple_bucket
        │   │   └───test
        │   │       ├───integration
        │   │       │   └───multiple_buckets
        │   │       └───setup
        │   └───gcs_buckets
        │       ├───.github
        │       │   └───workflows
        │       ├───build
        │       ├───docs
        │       ├───examples
        │       │   ├───multiple_buckets
        │       │   └───simple_bucket
        │       ├───helpers
        │       ├───modules
        │       │   └───simple_bucket
        │       └───test
        │           ├───integration
        │           │   └───multiple_buckets
        │           └───setup
        └───providers
            └───registry.terraform.io
                └───hashicorp
                    ├───archive
                    │   └───2.4.2
                    │       └───windows_amd64
                    ├───google
                    │   └───5.37.0
                    │       └───windows_amd64
                    └───random
                        └───3.6.2
                            └───windows_amd64
```
El lenguaje de programación principal para el presente reto fue Python usando el Framework de procesamiento distribuido Spark mediante el API PySpark. Este lenguaje provee una robusta variedad de funciones y métodos para limpiar, procesar y escribir grandes volúmenes de datos de forma escalable. Adicionalmente, cuenta con una gran comunidad de desarrollo.
Se desarrolló en Terraform la infraestructura como código necesaria para crear un workflow de Dataproc y así poder automatizar la ejecución de los jobs. 
Se requiere el cargue del archivo de trinos al bucket creado en el folder para tener el input disponible al código. Se realizó la prueba con el archivo pyspark_scripts\code\top_most_user_by_date.py. 
Adicionalmente, se deben ajustar los valores del proyecto de GCP donde se desee ejecutar el código. 

De igual forma, se creó un Dockerfile para tener disponible una aplicación contanerizada en caso de realizar pruebas en un local aisladamente. 

##Ejecución del código terraform

En caso de querer ejecutar la infraestructura definida en Terraform se sugiere utilizar el archivo exec.bash que automatiza los llamados init,plan y apply: 
```
bash exec.bash  --Ambientes Linux
```