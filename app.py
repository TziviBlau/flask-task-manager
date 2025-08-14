from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# חיבור למסד הנתונים
try:
    db = mysql.connector.connect(
        host="mysql",       # שם הקונטיינר של MySQL ב-docker-compose
        user="root",
        password="mypassword",
        database="Healthy"
    )
    cursor = db.cursor(dictionary=True)
    print("Database connected successfully")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    task_name = data.get("name")
    try:
        cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (task_name,))
        db.commit()
        return jsonify({"message": "Task added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
