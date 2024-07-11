#En el presente Dockerfile vamos a construir una aplicación portable para no utilizar el local 

FROM apache/spark-py:latest 

COPY . .

USER root 

RUN apt-get update -y &&\
    apt-get install -y python3.9 &&\
    pip3 install pyspark==3.4.0

EXPOSE 8080 7077 6066

CMD ["python3","top_most_user_by_date.py"]

