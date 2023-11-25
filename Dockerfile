FROM python:3.8-slim

WORKDIR /app

#Copying your application files to the container
COPY . /app

#Installing required Python packages
RUN pip install --no-cache-dir Faker Flask pandas sqlite_web  

ARG db=N
ARG login=N
ARG name=user
ARG pw=pw
ARG port=8080
ENV PORT=${port}
ENV DB=${db}
ENV LOGIN=${login}
ENV NAME=${name}
ENV PW=${pw}
#Installing SQLite3 for database interaction
#RUN my_db.py
#Command to run your Flask app
CMD ["python", "./hello.py"]