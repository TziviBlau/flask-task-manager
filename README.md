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

## ניתובים (Routes)

1. עמוד הבית
- URL: `/`
- Method: GET
- מה עושה: מציג את כל המשימות עם כפתורים ל־Toggle ול־Delete.
- קישור בדפדפן: http://localhost:5000/

2. בדיקת בריאות (Health Check)
- URL: `/health`
- Method: GET
- מה עושה: בודק אם השרת וה־DB פועלים.
- דוגמה ב־curl:
  curl http://localhost:5000/health
- קישור בדפדפן: http://localhost:5000/health

3. הוספת משימה
- URL: `/add`
- Method: POST
- פרמטרים: title (שם המשימה)
- מה עושה: מוסיף משימה חדשה למסד הנתונים.
- דוגמה ב־curl:
  curl -X POST -d "title=משימה חדשה" http://localhost:5000/add

4. שינוי סטטוס משימה (Toggle)
- URL: `/toggle/<task_id>`
- Method: GET
- מה עושה: משנה את סטטוס ההשלמה של המשימה.
- דוגמה ב־curl:
  curl http://localhost:5000/toggle/1
- קישור בדפדפן: http://localhost:5000/toggle/1

5. מחיקת משימה
- URL: `/delete/<task_id>`
- Method: GET
- מה עושה: מוחק את המשימה עם ה־ID הנתון.
- דוגמה ב־curl:
  curl http://localhost:5000/delete/1
- קישור בדפדפן: http://localhost:5000/delete/1



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
