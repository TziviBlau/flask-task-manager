from flask import Flask, render_template
import mysql.connector
import time
import os

app = Flask(__name__)

# קריאת משתני סביבה
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "taskuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "taskpass")
DB_NAME = os.environ.get("DB_NAME", "task_manager")

def get_db_connection():
    retries = 10
    while retries > 0:
        try:
            cnx = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return cnx
        except mysql.connector.Error:
            retries -= 1
            print("DB not ready, waiting 2 seconds...")
            time.sleep(2)
    raise Exception("Cannot connect to database after multiple retries")

def init_db():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    # יצירת טבלת משימות אם לא קיימת
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            done BOOLEAN DEFAULT FALSE
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

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
