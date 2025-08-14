from flask import Flask, render_template, request, redirect
import mysql.connector
import time

app = Flask(__name__)

def get_db_connection():
    retries = 10
    while retries > 0:
        try:
            cnx = mysql.connector.connect(
                host="db",
                user="root",
                password="",  # אין סיסמה
                database="task_manager"
            )
            return cnx
        except mysql.connector.Error:
            print("DB not ready, waiting 2 seconds...")
            retries -= 1
            time.sleep(2)
    raise Exception("Cannot connect to database after multiple retries")

def init_db():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)
    cnx.commit()
    cursor.close()
    cnx.close()

@app.route("/")
def index():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task_name = request.form["name"]
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (task_name,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
