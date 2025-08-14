from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# חיבור למסד הנתונים
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='mysql',  # שם הקונטיינר של MySQL ב-Docker Compose
            user='root',
            password='mypassword',
            database='task_manager'
        )
        return connection
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None

# דף הבית - הצגת המשימות
@app.route('/')
def index():
    connection = get_db_connection()
    tasks = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        cursor.close()
        connection.close()
    return render_template('index.html', tasks=tasks)

# יצירת משימה חדשה
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.form
    name = data.get('name')
    if not name:
        return jsonify({"error": "Task name required"}), 400

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (name,))
        connection.commit()
        cursor.close()
        connection.close()
    return jsonify({"message": "Task added successfully"}), 201

# מחיקת משימה לפי id
@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        connection.commit()
        cursor.close()
        connection.close()
    return jsonify({"message": "Task deleted successfully"}), 200

# עדכון משימה לפי id
@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "Task name required"}), 400

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE tasks SET name=%s WHERE id=%s", (name, task_id))
        connection.commit()
        cursor.close()
        connection.close()
    return jsonify({"message": "Task updated successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
