from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# פונקציה לחיבור לדטהבייס
def get_db_connection():
    return mysql.connector.connect(
        host="mysql_db",       # שם השירות של MySQL בקומפוז
        user="root",
        password="mypassword",
        database="task_manager"
    )

# עמוד ראשי -> מפנה לעמוד המשימות
@app.route('/')
def index():
    return redirect(url_for('tasks'))

# עמוד הצגת משימות
@app.route('/tasks')
def tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    all_tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('tasks.html', tasks=all_tasks)

# הוספת משימה
@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    if task_name.strip() != "":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (task_name,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
