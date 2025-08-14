from flask import Flask, render_template, request, redirect
import mysql.connector
import time
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mysecretpassword")
DB_NAME = os.getenv("DB_NAME", "task_manager")

def get_db_connection(retries=5, delay=3):
    for i in range(retries):
        try:
            cnx = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return cnx
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}, retrying ({i+1}/{retries})...")
            time.sleep(delay)
    raise Exception("Cannot connect to database after multiple retries")

def init_db():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL
        )
    """)
    cnx.commit()
    cursor.close()
    cnx.close()

@app.route("/")
def index():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template("tasks.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    if title:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        cnx.commit()
        cursor.close()
        cnx.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
