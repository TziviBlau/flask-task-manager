# Flask Task Manager

Simple Flask application with CRUD endpoints for managing tasks.

## Endpoints
- `GET /tasks` – Get all tasks
- `POST /tasks` – Add a task (JSON: `{"title": "Task name"}`)
- `PUT /tasks/<id>` – Mark task as done
- `DELETE /tasks/<id>` – Delete a task
- `GET /health` – Check app health

## Run Locally
```bash
pip install -r requirements.txt
python app.py
