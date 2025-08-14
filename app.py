from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
import time

app = Flask(__name__)

# פונקציה להתחברות למסד הנתונים עם Retry
def get_db_connection(retries=5, delay=5):
    for i in range(retries):
        try:
            connection = mysql.connector.connect(
                host="mysql",      # שם ה-Service ב-Docker Compose
                user="root",
                password="mypassword",
                database="Healthy"
            )
            print("Connected to MySQL database")
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            time.sleep(delay)
    raise Exception("Could not connect to MySQL database after multiple attempts")

# יצירת חיבור גלובלי
db = get_db_connection()

@app.route("/")
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task_name = request.form.get("task")
    if task_name:
        cursor = db.cursor()
        cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (task_name,))
        db.commit()
        cursor.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()
    cursor.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
