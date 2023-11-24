
#!/bin/bash
name='user'
port=8000
pw='pw'
db='N'
l='N'
while getopts n:p:w:d:l: flag
do
    case "${flag}" in
        n) name=${OPTARG};;
        p) port=${OPTARG};;
        w) pw=${OPTARG};;
        d) db=${OPTARG};;
        l) login=${OPTARG};;
    esac
done
echo $db
echo $login
echo $name
echo $pw
echo $port

sudo docker build --build-arg db=$db --build-arg login=$login --build-arg name=$name --build-arg pw=$pw --build-arg port=$port -t hello-world .

sudo docker run --name test -p $port:8080 -v /home/thomas/Desktop/progettoCyber:/app hello-world

sqlite_web -P -r people.db 
