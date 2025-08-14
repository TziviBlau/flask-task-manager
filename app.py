from flask import Flask, render_template
import mysql.connector
import time

app = Flask(__name__)

DB_HOST = "mysql_db"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "task_db"

def get_db_connection():
    for _ in range(15):
        try:
            cnx = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return cnx
        except mysql.connector.Error:
            print("DB not ready, waiting 2 seconds...")
            time.sleep(2)
    raise Exception("Cannot connect to database after multiple retries")

def init_db():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            completed BOOLEAN DEFAULT FALSE
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
    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
