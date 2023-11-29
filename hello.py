from flask import Flask, jsonify
import sqlite3

from faker import Faker
import pandas as pd
import os 
import subprocess

import csv

app = Flask(__name__)
fake = Faker()


def import_database():
    csv_file = os.getenv('FILE')
    print(csv_file)
    # Connessione al database SQLite
    conn = sqlite3.connect('people.db')

    # Creazione di un cursore
    cursor = conn.cursor()
   
    # Leggo il file CSV per ottenere i nomi delle colonne e delle tables
    with open(csv_file, newline='') as file:
        csv_reader = csv.reader(file)
        table_data={}
        header = next(csv_reader)  # Ottengo l'intestazione
        
        print("header :"+ str(header))
        # Query per ottenere i nomi delle tabelle
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

    # Ottengo il nome del file senza l'estensione per usare come nome della tabella
    table_name = csv_file.split('.')[1]

    # Costruisco la query per creare la tabella dinamicamente
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} TEXT' for col in header])})"
    print(create_table_query)
    cursor.execute(create_table_query)


    # Inserisco i dati nella tabella
    with open(csv_file, newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Salto l'intestazione
        cursor.executemany(f"INSERT INTO {table_name} VALUES ({', '.join(['?']*len(header))})", csv_reader)

    # Commit delle modifiche
    conn.commit()

    # Chiusura della connessione
    conn.close()

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
    print(DB_esitente)
    if DB_esitente == "N":
       print("creating DB")
       create_database()
    else:
        import_database()
        print("importing DB")
    #comando = "docker cp test:/app/people.db /home/thomas/Desktop/progettoCyber/people.db"
    #output = subprocess.run(comando, shell=True)
    
    #app.run(debug=True, host='0.0.0.0')


    
