from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import time

app = Flask(__name__)

# --- פונקציות חיבור למסד הנתונים ---
def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            connection = mysql.connector.connect(
                host=os.environ.get("MYSQL_HOST", "db"),
                user=os.environ.get("MYSQL_USER", "root"),
                password=os.environ.get("MYSQL_PASSWORD", "mysecretpassword"),
                database=os.environ.get("MYSQL_DATABASE", "task_manager")
            )
            return connection
        except mysql.connector.Error as e:
            print(f"Database connection failed: {e}, retrying...")
            retries -= 1
            time.sleep(3)
    raise Exception("Cannot connect to database after multiple retries")

def init_db():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE
        )
    """)
    cnx.commit()
    cursor.close()
    cnx.close()

init_db()

# --- מסלולים ---
@app.route("/")
def index():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template("tasks.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    description = request.form.get("description")
    if title:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
        cnx.commit()
        cursor.close()
        cnx.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    title = request.form.get("title")
    description = request.form.get("description")
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("UPDATE tasks SET title=%s, description=%s WHERE id=%s", (title, description, task_id))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for("index"))

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("SELECT completed FROM tasks WHERE id=%s", (task_id,))
    result = cursor.fetchone()
    if result:
        new_status = not result[0]
        cursor.execute("UPDATE tasks SET completed=%s WHERE id=%s", (new_status, task_id))
        cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for("index"))

# --- הרצת האפליקציה ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
