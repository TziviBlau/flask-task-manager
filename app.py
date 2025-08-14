from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# רשימת משימות התחלתית
tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build CI/CD pipeline", "done": False}
]

# עמוד ראשי – מציג את ממשק ה־HTML
@app.route("/")
def home():
    return render_template("index.html")

# בריאות האפליקציה / בדיקת DB
@app.route("/health")
def health():
    # כאן בגרסה הפשוטה – database always healthy
    return jsonify({"database": "Healthy", "status": "OK"})

# קבלת כל המשימות
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

# הוספת משימה חדשה
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    new_id = max([t["id"] for t in tasks] + [0]) + 1
    task = {"id": new_id, "title": data["title"], "done": False}
    tasks.append(task)
    return jsonify(task), 201

# סימון משימה כבוצעה
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def mark_task_done(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

# מחיקת משימה
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"result": "Task deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
