import os
from flask import Flask, jsonify, request, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# חיבור למסד הנתונים
try:
    db = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "mypassword"),
        database=os.getenv("MYSQL_DATABASE", "Healthy")
    )
    cursor = db.cursor(dictionary=True)
    print("Database connected successfully!")
except Error as e:
    print(f"Error connecting to MySQL: {e}")
    db = None
    cursor = None

# דף הבית - מציג את המשימות
@app.route("/")
def index():
    if cursor:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    else:
        tasks = []
    return render_template("index.html", tasks=tasks)

# קבלת כל המשימות ב-JSON
@app.route("/tasks", methods=["GET"])
def get_tasks():
    if cursor:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return jsonify(tasks)
    return jsonify({"error": "Database not connected"}), 500

# יצירת משימה חדשה
@app.route("/tasks", methods=["POST"])
def add_task():
    if cursor:
        data = request.json
        task_name = data.get("title")
        done = data.get("done", False)
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", (task_name, done))
        db.commit()
        return jsonify({"message": "Task added!"}), 201
    return jsonify({"error": "Database not connected"}), 500

# עדכון משימה
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if cursor:
        data = request.json
        done = data.get("done")
        cursor.execute("UPDATE tasks SET done=%s WHERE id=%s", (done, task_id))
        db.commit()
        return jsonify({"message": "Task updated!"})
    return jsonify({"error": "Database not connected"}), 500

# מחיקת משימה
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if cursor:
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        db.commit()
        return jsonify({"message": "Task deleted!"})
    return jsonify({"error": "Database not connected"}), 500

# הפעלה
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
