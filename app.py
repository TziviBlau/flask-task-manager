from flask import Flask, render_template, request, redirect
import mysql.connector
import time

app = Flask(__name__)

# חיבור למסד הנתונים - בלי סיסמאות
def get_db_connection():
    retries = 5
    while retries:
        try:
            cnx = mysql.connector.connect(
                host="db",
                user="root",
                password="",
                database="task_manager"
            )
            return cnx
        except mysql.connector.Error:
            retries -= 1
            time.sleep(2)
    raise Exception("Cannot connect to database")

@app.route("/")
def index():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)
    
    # יוצרים את הטבלה אם לא קיימת
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cnx.commit()
    
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    description = request.form.get("description")

    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
