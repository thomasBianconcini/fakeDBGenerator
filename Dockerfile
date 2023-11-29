FROM python:3.8-slim

WORKDIR /app

#Copying your application files to the container
COPY . /app

#Installing required Python packages
RUN pip install --no-cache-dir Faker Flask pandas sqlite_web  

ARG db=N
ARG port=8080
ARG file=null
ENV PORT=${port}
ENV DB=${db}
ENV FILE=${file}

#Installing SQLite3 for database interaction
#RUN my_db.py
#Command to run your Flask app
CMD ["python", "./hello.py"]
