# Flask Task Manager

יישום לניהול משימות (To-Do / Task Manager) שנבנה עם Flask ו-MySQL ומופעל באמצעות Docker Compose. האפליקציה מאפשרת ליצור, לצפות, לעדכן ולמחוק משימות (CRUD) בצורה פשוטה ואינטואיטיבית. היא כוללת ממשק אינטרנטי בסיסי, API REST עם נקודות קצה לפעולות על המשימות ובדיקת בריאות (Health Check) עם התחברות למסד הנתונים. 

## פיצ'רים
- הוספה, עריכה ומחיקה של משימות
- סימון משימה כהושלמה
- ממשק HTML/CSS בסיסי
- API REST עם נקודות קצה: GET /, POST /add, PUT /toggle/<id>, DELETE /delete/<id>
- בדיקת בריאות במסד הנתונים ב-/health
- תמיכה בהרצה מלאה עם Docker Compose

## ארכיטקטורה
המערכת בנויה משלוש שכבות: 
1. **MySQL** – מסד הנתונים עם volume קבוע לשמירה על נתונים.
2. **Flask App** – שרת האפליקציה שמבצע את כל פעולות CRUD ומאזין ב־5000.
3. **Nginx** – משמש כ-reverse proxy ומאזן עומסים, מאזין ב־8080.

## התקנה והרצה
### דרישות
- Docker
- Docker Compose

### צעדים
1. שיבוט הפרויקט:
   ```bash
   git clone https://github.com/your-username/flask-task-manager.git
   cd flask-task-manager
הרצת האפליקציה:

bash
Copy
Edit
docker compose up --build -d
בדיקת בריאות:

bash
Copy
Edit
curl http://localhost:5000/health
התגובה צריכה להיות "OK".

צפייה בממשק בדפדפן: פתחי http://localhost:5000/.

פעולות API לדוגמה:

קבלת רשימת משימות: curl http://localhost:5000/

הוספת משימה: curl -X POST -d "title=משימה חדשה" http://localhost:5000/add

סימון משימה כהושלמה: curl http://localhost:5000/toggle/1

מחיקת משימה: curl http://localhost:5000/delete/1

CI/CD
הפרויקט כולל pipeline עם 6 שלבים ב-GitHub Actions: Build, Test, Package, E2E Test, Push ל-DockerHub ו-Deploy ל-Killercoda. צילומי מסך של pipeline מוצלחת ושורת הפקודות יכולים להציג את הצלחת כל השלבים.

בדיקות מקומיות
Health check: curl http://localhost:5000/health מחזיר "OK".

CRUD פונקציות נבדקות עם פקודות curl.

ווידוא שמירה על נתונים אחרי הפסקת הקונטיינרים והפעלתם מחדש.

שימוש ב-Docker Compose
קובץ docker-compose.yml מגדיר שלושה קונטיינרים: mysql, flask app ו-network.

Volume של MySQL שומר את הנתונים גם לאחר restart.

מבנה התיקיות
swift
Copy
Edit
flask-task-manager/
├── .github/workflows/
│   └── ci-cd-pipeline.yml
├── static/
│   └── style.css
├── templates/
│   └── tasks.html
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
סיכום
הפרויקט מדגים יכולת לפתח אפליקציה מלאה עם Flask, חיבור למסד נתונים, שימוש ב-Docker Compose, וליישם תהליכי CI/CD מקצועיים. כל הניתובים, ה-API וה-UI נבדקו ופועלים בהצלחה. נלמדו מיומנויות עבודה עם multi-tier architecture, persistent storage, ו-automation עם GitHub Actions.

markdown
Copy
Edit
