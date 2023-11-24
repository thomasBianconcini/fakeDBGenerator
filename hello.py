from flask import Flask, jsonify
import sqlite3
from flask_httpauth import HTTPBasicAuth
from faker import Faker
import pandas as pd
import os 
import subprocess

app = Flask(__name__)
fake = Faker()
auth = HTTPBasicAuth()

users = {
    "admin": "password",
    # Add more users here if needed
}

def query_db(query, args=(), one=False):
    con = sqlite3.connect('people.db')
    df = pd.read_sql_query(query, con)
    con.close()
    return df.to_html()

def get_data():
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM people')
    data = cursor.fetchall()
    conn.close()
    return data


def create_database():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS people''')
    c.execute('''DROP TABLE IF EXISTS details''')
    c.execute('''CREATE TABLE people (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    surname TEXT)''')
    c.execute('''CREATE TABLE details (
                    person_id INTEGER,
                    date_of_birth TEXT,
                    city TEXT,
                    FOREIGN KEY(person_id) REFERENCES people(id))''')

    for _ in range(100):  # Adjust for fewer entries
        c.execute("INSERT INTO people (name, surname) VALUES (?, ?)", 
                  (fake.first_name(), fake.last_name()))

    conn.commit()

    c.execute("SELECT id FROM people")
    people_ids = c.fetchall()
    for person_id in people_ids:
        c.execute("INSERT INTO details (person_id, date_of_birth, city) VALUES (?, ?, ?)", 
                  (person_id[0], fake.date_of_birth(), fake.city()))

    conn.commit()
    conn.close()

    # Return the table as an HTML response
    
if __name__ == '__main__':
    DB_esitente = os.getenv('DB')
    if DB_esitente == "N":
        login = os.getenv('LOGIN')
        if login == 'S':
            name= os.getenv('NAME')
            pw= os.getenv('PW')
            users={
                name : pw,
            }
        else:
             users={
                "admin": "password",
            }
    elif DB_esitente == "S":
        cc="ciao"

    create_database()
    #comando = "docker cp test:/app/people.db /home/thomas/Desktop/progettoCyber/people.db"
    #output = subprocess.run(comando, shell=True)
    
    #app.run(debug=True, host='0.0.0.0')


    
