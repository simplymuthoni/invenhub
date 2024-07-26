import os
import mariadb
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from mariadb import Error

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+mariadbconnector://mugo:Demo123@127.0.0.1:3306/hope"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

def create_connection():
    conn = None
    try:
        conn = mariadb.connect(
            user="mugo",
            password="Demo123",
            host="127.0.0.1",
            port=3306,
            database="hope"
        )
    except Error as e:
        print(f"Error: {e}")
    return conn

def create_tables():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS user(
                            id CHAR(36) PRIMARY KEY,
                            username VARCHAR(20) NOT NULL,
                            name VARCHAR(30) NOT NULL,
                            password VARCHAR(10) NOT NULL,
                            email VARCHAR(30) NOT NULL,
                            phone_number VARCHAR(12) NOT NULL,
                            address VARCHAR(30) NOT NULL);''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS admin(
                            adminid CHAR(36) PRIMARY KEY,
                            email VARCHAR(20) NOT NULL,
                            name VARCHAR(30) NOT NULL,
                            password VARCHAR(10) NOT NULL);''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS clothes(
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(50),
                            description TEXT,
                            price FLOAT);''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS cart (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            clothes_id INT NOT NULL,
                            user_id CHAR(36) NOT NULL,
                            quantity INT NOT NULL DEFAULT 1,
                            FOREIGN KEY (clothes_id) REFERENCES clothes(id),
                            FOREIGN KEY (user_id) REFERENCES user(id));''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS payment (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            user_id CHAR(36) NOT NULL,
                            amount FLOAT NOT NULL,
                            payment_method ENUM('credit_card', 'paypal', 'bank_transfer') NOT NULL,
                            payment_status ENUM('pending', 'success', 'failed') NOT NULL,
                            payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES user(id));''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                            id CHAR(36) PRIMARY KEY,
                            user_id CHAR(36) NOT NULL,
                            feedback_text TEXT NOT NULL,
                            feedback_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES user(id));''')

        conn.commit()
        cursor.close()
        conn.close()

def init_db():
    create_tables()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
