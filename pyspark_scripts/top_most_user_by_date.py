import pyspark.sql.functions as F
from pyspark.sql.functions import *
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import row_number
from pyspark.sql.functions import get_json_object

if __name__ == "__main__":

    # Para las pruebas se usar local[*] así utiliza todos los threads de la máquina en ambiente productivo se usa YARN.
    conf = SparkConf().setMaster("local[*]").setAppName("Dataframe_examples")
    sc = SparkContext(conf=conf)

    spark = SparkSession(sc)

    # Lectura del archivo que contiene los JSON
    df = spark.read.text("farmers-protest-tweets-2021-2-4.json")

    """"
    Para el primer ejercicio nos interesa hacer parse de las fechas y el username dado que queremos conocer 
    la fecha con mayores trinos y el usuario que mas trino respectivamente
    """
    df = df.select(
        get_json_object(df.value, "$.user.username").alias("username"),
        get_json_object(df.value, "$.date").cast("date").alias("date"),
    ).createOrReplaceTempView("dates_users")

    """
    Se utiliza spark SQL por la practicidad. Pasos a realizar mediante CTEs: 
    1. Fecha , username y conteo total por usuario y agrupación 
    2. Fecha, username y la suma de los conteos de trinos para obtener el total por fecha 
    3. Creación de una window function de row number para enumerar el usuario con mas interacciones y en la fecha con más trinos
    4. Se filtra la window function con = 1 para obtener el usuario que más trinó en cada fecha 
    """
    df = spark.sql(
    """
    With
        first as (
        select
        date,
        username,
        count(1) as total_by_user
        from dates_users
        group by date,username
        ),
        total_by_user as(
        select
        date,
        username,
        total_by_user,
        sum(total_by_user) over(partition by date) as total_date
        from first
        ), 
        rank_users as (
        select
        date,
        username,
        total_by_user,
        total_date,
        row_number() over(partition by date order by total_date,total_by_user desc) as row_numm
        from total_by_user 
        ), 
        last as (
        select 
        date,
        total_date,
        total_by_user,
        username
        from rank_users
        where row_numm = 1 
        ) 
        select 
        date,
        username
        from last
        order by total_date desc, total_by_user desc

    """
    )

    """
    Se necesita un output en formato :
    [(datetime.date(2021, 2, 12), 'RanbirS00614606'),
    (datetime.date(2021, 2, 13), 'MaanDee08215437')] 
    """
    rdd = df.rdd 
    
    # Convertir el RDD a una tuple mediante map
    data = rdd.map(tuple) 
    
    # Mostrar los datos
    print(data.collect())
