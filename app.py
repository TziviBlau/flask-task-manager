from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASS", "password"),
    database=os.environ.get("DB_NAME", "tasks_db")
)
cursor = db.cursor(dictionary=True)

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    done BOOLEAN DEFAULT FALSE
)
""")
db.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (data["title"],))
    db.commit()
    return jsonify({"message": "Task added"}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    cursor.execute("UPDATE tasks SET done=%s WHERE id=%s", (data["done"], task_id))
    db.commit()
    return jsonify({"message": "Task updated"})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    db.commit()
    return jsonify({"message": "Task deleted"})

@app.route("/health")
def health():
    try:
        cursor.execute("SELECT 1")
        return jsonify({"status": "OK", "database": "Healthy"})
    except:
        return jsonify({"status": "FAIL", "database": "Unhealthy"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
