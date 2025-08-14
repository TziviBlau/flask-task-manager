from flask import Flask, render_template, request, redirect
import mysql.connector
import os
import time

app = Flask(__name__)

# חיבור לדטהבייס עם retries עד שה־DB מוכן
def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASSWORD', ''),
                database=os.environ.get('DB_NAME', 'task_manager')
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            retries -= 1
            time.sleep(3)
    raise Exception("Cannot connect to MySQL after several retries.")

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')
    if task_name:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (task_name,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
