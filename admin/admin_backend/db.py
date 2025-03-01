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
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    return conn

# Create a MongoClient instance
client = MongoClient(os.getenv('MONGO_DB_URL'))
# Get a reference to the database
mongodb= client['hackmatrixdb']

def get_mongo_connection():
    """
    Returns a reference to the MongoDB database.

    Returns:
        pymongo.database.Database: A reference to the MongoDB database.
    """
    return mongodb
