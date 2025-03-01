import sqlite3
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

def get_rdbms_connection():
    """
    Establishes a connection to the SQLite database and creates the 'users' table if it does not exist.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create a MongoClient instance
client = MongoClient(os.getenv('MONGO_DB_URL'))
mongodb = client['test']

def get_mongo_connection():
    return mongodb

def db_inits():
    collection_name = 'job_postings'
    if collection_name in mongodb.list_collection_names():
        print(f"Collection '{collection_name}' already exists.")
    else:
        mongodb.create_collection(collection_name)
        print(f"Collection '{collection_name}' created successfully!")
    
    conn = get_rdbms_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            userid INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS applns (
            applnid INTEGER PRIMARY KEY AUTOINCREMENT,
            jobid TEXT NOT NULL,
            userid TEXT NOT NULL,
            at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            shortlisted VARCHAR(3) NOT NULL DEFAULT 'NO'
        )
    ''')
    conn.commit()
    cur.close()