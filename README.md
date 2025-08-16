# Flask Task Manager

יישום פשוט לניהול משימות (To-Do / Task Manager) שנבנה עם **Flask** ו־**MySQL**, ומריץ סביבה מלאה בעזרת **Docker Compose**.  
האפליקציה מאפשרת לנהל רשימת משימות עם יכולות CRUD מלאות: יצירה, צפייה, עדכון ומחיקה.

---

##  פיצ'רים
- הוספה, עריכה ומחיקה של משימות
- סימון משימה כהושלמה
- ממשק אינטרנטי בסיסי עם HTML/CSS
- API REST עם 4 נקודות קצה עיקריות (GET, POST, PUT, DELETE)
- בדיקת בריאות (Health Check) עם התחברות למסד הנתונים
- תמיכה ב־Docker להרצה פשוטה בכל סביבה

---

##  ארכיטקטורה
המערכת מבוססת על 3 שכבות:
1. **Nginx** – משמש כ־reverse proxy ומאזן עומסים (מאזין ב־`localhost:8080`)
2. **Flask App** – שרת האפליקציה (מאזין ב־`5000`)
3. **MySQL** – מסד נתונים מאוחסן עם volume קבוע לשמירה על נתונים

---

## התקנה והרצה

### דרישות מקדימות
- Docker
- Docker Compose

### שלבים
1. שיבוט הפרויקט:
   ```bash
   git clone https://github.com/your-username/flask-task-manager.git
   cd flask-task-manager
   ```

2. הפעלת הסביבה:
   ```bash
   cd docker-compose
   docker-compose up -d
   ```

3. גישה לאפליקציה:
   ```
   http://localhost:8080
   ```

---

## 🧪 בדיקות עם curl
במקום טסטים מורכבים, ניתן לבדוק את האפליקציה בפקודות curl פשוטות:

```bash
# בדיקת בריאות
curl -f http://localhost:8080/health

# קבלת רשימת משימות
curl -f http://localhost:8080/api/tasks

# הוספת משימה
curl -X POST -H "Content-Type: application/json"     -d '{"title": "לסיים פרויקט", "completed": false}'     http://localhost:8080/api/tasks

# סימון משימה כהושלמה
curl -X PUT -H "Content-Type: application/json"     -d '{"completed": true}'     http://localhost:8080/api/tasks/1

# מחיקת משימה
curl -X DELETE http://localhost:8080/api/tasks/1
```

---

## 📂 מבנה הפרויקט
```
flask-task-manager/
├── .github/workflows/
│ └── ci-cd-pipeline.yml
├── static/
│ └── style.css
├── templates/
│ └── tasks.html
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🛠️ טכנולוגיות בשימוש
- **Python 3 + Flask**
- **MySQL 8**
- **Nginx**
- **Docker & Docker Compose**

---

## 📖 סיכום
הפרויקט מדגים כיצד ניתן לבנות אפליקציית ווב בסיסית עם מסד נתונים אמיתי,  
לעטוף אותה בסביבה מודולרית בעזרת Docker Compose,  
ולבדוק אותה באמצעות פקודות curl פשוטות מקצה לקצה.
