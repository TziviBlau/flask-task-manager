from flask import Flask, jsonify, request, render_template
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# חיבור ל-MySQL דרך משתני סביבה
try:
    db = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASS", ""),
        database=os.environ.get("DB_NAME", "tasks_db")
    )
    cursor = db.cursor(dictionary=True)
except Error as e:
    print(f"Error connecting to MySQL: {e}")
    db = None
    cursor = None

# יצירת טבלת משימות אם לא קיימת
if db:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    db.commit()

# דף הבית
@app.route("/")
def index():
    if not db:
        return "Database not connected"
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

# Health check
@app.route("/health")
def health():
    if db:
        try:
            cursor.execute("SELECT 1")
            return jsonify({"status": "OK", "database": "Healthy"})
        except:
            return jsonify({"status": "OK", "database": "Unhealthy"})
    else:
        return jsonify({"status": "OK", "database": "Unhealthy"})

# קבלת כל המשימות
@app.route("/tasks", methods=["GET"])
def get_tasks():
    if not db:
        return jsonify({"error": "Database not connected"}), 500
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return jsonify(tasks)

# יצירת משימה חדשה
@app.route("/tasks", methods=["POST"])
def add_task():
    if not db:
        return jsonify({"error": "Database not connected"}), 500
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing title"}), 400
    cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", (data["title"], False))
    db.commit()
    return jsonify({"id": cursor.lastrowid, "title": data["title"], "done": False}), 201

# עדכון משימה
@app.route("/tasks/<int:task_id>", methods=["PUT", "PATCH"])
def update_task(task_id):
    if not db:
        return jsonify({"error": "Database not connected"}), 500
    data = request.get_json()
    cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
    task = cursor.fetchone()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    title = data.get("title", task["title"])
    done = data.get("done", task["done"])
    cursor.execute("UPDATE tasks SET title=%s, done=%s WHERE id=%s", (title, done, task_id))
    db.commit()
    return jsonify({"id": task_id, "title": title, "done": done})

# מחיקת משימה
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if not db:
        return jsonify({"error": "Database not connected"}), 500
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    db.commit()
    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
