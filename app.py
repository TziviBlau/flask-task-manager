import os
import time
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# פונקציה להתחברות ל־DB עם retries
def get_db_connection(retries=5, delay=3):
    for attempt in range(retries):
        try:
            connection = mysql.connector.connect(
                host=os.environ.get("MYSQL_HOST", "db"),
                user=os.environ.get("MYSQL_USER", "root"),
                password=os.environ.get("MYSQL_PASSWORD", "mysecretpassword"),
                database=os.environ.get("MYSQL_DATABASE", "task_manager")
            )
            return connection
        except Error as e:
            print(f"Database connection failed: {e}, retrying ({attempt+1}/{retries})...")
            time.sleep(delay)
    raise Exception("Cannot connect to database after multiple retries")

# אתחול DB - יצירת טבלה אם לא קיימת
def init_db():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    cnx.commit()
    cursor.close()
    cnx.close()

@app.route('/')
def index():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('tasks.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if title:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        cnx.commit()
        cursor.close()
        cnx.close()
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("UPDATE tasks SET done = NOT done WHERE id = %s", (task_id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
