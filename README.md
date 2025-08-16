# Flask Task Manager

יישום לניהול משימות (To-Do / Task Manager) שנבנה עם **Flask** ו-**MySQL** ומופעל באמצעות **Docker Compose**. האפליקציה מאפשרת ליצור, לצפות, לעדכן ולמחוק משימות (CRUD) בצורה פשוטה ואינטואיטיבית. היא כוללת ממשק אינטרנטי בסיסי, **API REST** עם נקודות קצה לפעולות על המשימות ובדיקת בריאות (Health Check) עם התחברות למסד הנתונים. 

---

## ✨ פיצ'רים
- הוספה, עריכה ומחיקה של משימות
- סימון משימה כהושלמה
- ממשק HTML/CSS בסיסי
- API REST עם נקודות קצה:
  - `GET /` – קבלת רשימת כל המשימות
  - `POST /add` – הוספת משימה חדשה
  - `GET /toggle/<id>` – סימון משימה כהושלמה/לא מושלמת
  - `GET /delete/<id>` – מחיקת משימה
- בדיקת בריאות במסד הנתונים: `GET /health`
- תמיכה בהרצה מלאה עם Docker Compose

---

## 🏗️ ארכיטקטורה
המערכת בנויה משלוש שכבות:  
1. **MySQL** – מסד הנתונים עם **volume קבוע** לשמירה על נתונים גם אחרי הפעלה מחדש של הקונטיינרים.  
2. **Flask App** – שרת האפליקציה שמבצע את כל פעולות CRUD ומאזין ב־5000.  
3. **Nginx** – משמש כ-reverse proxy ומאזן עומסים, מאזין ב־8080.

---

## 🚀 התקנה והרצה
### דרישות
- Docker
- Docker Compose

### שלבים
1. שיבוט הפרויקט:
```bash
git clone https://github.com/your-username/flask-task-manager.git
cd flask-task-manager
```

2. הרצת האפליקציה:
```bash
docker compose up --build -d
```

3. בדיקת בריאות:
```bash
curl http://localhost:5000/health
```
התשובה צריכה להיות `"OK"`.

4. צפייה בממשק בדפדפן:  
[http://localhost:5000/](http://localhost:5000/)

5. פעולות API נוספות:
- קבלת רשימת משימות:
```bash
curl http://localhost:5000/
```
- הוספת משימה:
```bash
curl -X POST -d "title=משימה חדשה" http://localhost:5000/add
```
- סימון משימה כהושלמה:
```bash
curl http://localhost:5000/toggle/1
```
- מחיקת משימה:
```bash
curl http://localhost:5000/delete/1
```

---

## 📁 מבנה התיקיות
```
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
```

---

## ⚙️ CI/CD
הפרויקט כולל **pipeline עם 6 שלבים** ב-GitHub Actions: Build, Test, Package, E2E Test, Push ל-DockerHub ו-Deploy ל-Killercoda. ניתן להראות צילומי מסך של ה-pipeline המוצלחת כדי להציג את הצלחת כל השלבים.

---

## ✅ בדיקות מקומיות
- Health check:  
```bash
curl http://localhost:5000/health
```
- CRUD פונקציות נבדקות עם פקודות `curl`.  
- ווידוא שמירה על נתונים אחרי הפסקת הקונטיינרים והפעלתם מחדש.

---

## 💡 סיכום
הפרויקט מדגים יכולת לפתח אפליקציה מלאה עם Flask, חיבור למסד נתונים, שימוש ב-Docker Compose, וליישם תהליכי CI/CD מקצועיים. כל הניתובים, ה-API וה-UI נבדקו ופועלים בהצלחה. נלמדו מיומנויות עבודה עם multi-tier architecture, persistent storage, ו-automation עם GitHub Actions.
