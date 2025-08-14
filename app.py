from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error
import os
import time

app = Flask(__name__)

# פונקציה לקבלת חיבור לדאטהבייס
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
        except Error as e:
            print(f"Database connection failed: {e}, retrying...")
            retries -= 1
            time.sleep(2)
    raise Exception("Cannot connect to database after multiple retries")

# יצירת טבלה אם היא לא קיימת
def init_db():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT
        )
    """)
    cnx.commit()
    cursor.close()
    cnx.close()

init_db()

# עמוד הבית / הצגת משימות
@app.route('/tasks')
def tasks():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks_list = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('tasks.html', tasks=tasks_list)

# הוספת משימה חדשה
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('/tasks')
    return render_template('add_task.html')

# מחיקת משימה
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('/tasks')
    except Exception as e:
        return f"Error deleting task: {e}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
