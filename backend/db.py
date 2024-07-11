import os
import mariadb
from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from mariadb import Error
from app import config
import app

app.Config["SQLALCHEMY_DATABASE_URI"] = "mariadb+mariadbconnector://mugo:Demo123@127.0.0.1:3306/hope"

db = SQLAlchemy(app)


def create_connection():
    
    conn = None
    try:
        conn = mariadb.connect(db)
    except Error as e:
        print(e)
    return conn

def create_tables():

    conn = create_connection()
    if conn is not None:
        
        conn.execute('''CREATE TABLE IF NOT EXISTS user(
                            id CHAR(36) PRIMARY KEY,
                            username VARCHAR(20) NOT NULL,
                            name VARCHAR(30) NOT NULL,
                            password VARCHAR(10) NOT NULL,
                            email VARCHAR(30) NOT NULL,
                            phone_number VARCHAR(12) NOT NULL,
                            address VARCHAR(30) NOT NULL);''')
        
        conn.commit()
        conn.close()

def init_db():
    
    create_tables()