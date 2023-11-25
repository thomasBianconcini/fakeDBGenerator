#!/bin/bash
port=8080
db='N'

while getopts p:d: flag
do
    case "${flag}" in
        p) port=${OPTARG};;
        d) db=${OPTARG};;
    esac
done
echo $db
echo $port

sudo docker build --build-arg db=$db --build-arg port=$port -t hello-world .

sudo docker run --name test -p $port:8080 -v /home/thomas/Desktop/progettoCyber:/app hello-world

sqlite_web -P -r -p $port people.db 
