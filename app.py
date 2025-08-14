from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# רשימת משימות לדוגמה
tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build CI/CD pipeline", "done": False}
]

# דף הבית
@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)

# Health check
@app.route("/health")
def health():
    return jsonify({"status": "OK", "database": "Healthy"})

# קבלת כל המשימות
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

# יצירת משימה חדשה
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing title"}), 400
    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": data["title"],
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# עדכון משימה (סימון כבוצעה או שינוי כותרת)
@app.route("/tasks/<int:task_id>", methods=["PUT", "PATCH"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    if "title" in data:
        task["title"] = data["title"]
    if "done" in data:
        task["done"] = data["done"]
    return jsonify(task)

# מחיקת משימה
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    # מאזין על כל הכתובות, פורט 5000
    app.run(host="0.0.0.0", port=5000)
