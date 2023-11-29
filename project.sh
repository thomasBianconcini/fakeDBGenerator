#!/bin/bash
port=8080
db='N'
f='null'
while getopts p:d:f: flag
do
    case "${flag}" in
        p) port=${OPTARG};;
        d) db=${OPTARG};;
        f) f=${OPTARG};;
    esac
done
echo $db
echo $port
echo $f

sudo docker build --build-arg db=$db --build-arg port=$port --build-arg file=$f -t hello-world .

sudo docker run -p $port:8080 -v /home/thomas/Desktop/progettoCyber:/app hello-world

sqlite_web -P -r -p $port people.db 

