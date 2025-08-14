from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "db"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", "mysecretpassword"),
        database=os.environ.get("MYSQL_DATABASE", "task_manager")
    )

@app.route("/tasks")
def tasks():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks_list = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template("tasks.html", tasks=tasks_list)

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description", "")
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect("/tasks")
    return render_template("add_task.html")

@app.route("/delete/<int:id>", methods=["POST"])
def delete_task(id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect("/tasks")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
