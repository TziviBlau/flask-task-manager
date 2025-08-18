# 📌 Flask Task Manager

יישום לניהול משימות (**Task Manager**) שנבנה עם **Flask** ו־**MySQL**, ומשתמש ב־**Docker Compose**, **Kubernetes** ו־**CI/CD (GitHub Actions)** לניהול, פרישה ובדיקות.  
האפליקציה מאפשרת ניהול משימות עם יכולות CRUD מלאות: יצירה, צפייה, עדכון ומחיקה.

---

## ✨ פיצ'רים  
- ✅ הוספה, עריכה ומחיקה של משימות  
- ✅ סימון משימות כהושלמו  
- ✅ ממשק אינטרנטי בסיסי עם HTML/CSS  
- ✅ API REST עם נקודות קצה עיקריות: `GET`, `POST`, `PUT`, `DELETE`  
- ✅ בדיקת בריאות (Health Check) עם התחברות למסד הנתונים  
- ✅ תמיכה מלאה ב־Docker להרצה מקומית  
- ✅ פרישה מלאה על Kubernetes עם StatefulSet עבור MySQL ו־Persistent Volume  
- ✅ בדיקות התמדה של נתונים לאחר אתחול מחדש של הפודים  

---

## 🏗️ ארכיטקטורה  
המערכת מבוססת על 3 שכבות עיקריות:  

1. **Flask App** – שרת האפליקציה (מאזין בפורט 5000)  
2. **MySQL** – מסד נתונים עם Persistent Volume לשמירה על נתונים  
3. **Kubernetes** – פרישה מלאה הכוללת Deployments, Services ו־StatefulSet  

### תרשים ארכיטקטורה (ASCII)  

```
           +-------------------+
           |   User / Browser  |
           +-------------------+
                    |
                    v
           +-------------------+
           |    Flask App      |
           | (Deployment + SVC)|
           +-------------------+
                    |
                    v
           +-------------------+
           |      MySQL        |
           | (StatefulSet + PV)|
           +-------------------+
```

---

## 🚀 התקנה והרצה  

### דרישות מקדימות  
- Docker  
- Docker Compose  
- kubectl (לפרישה ל־Kubernetes / Killercoda)  

### הרצה מקומית עם Docker Compose  
`git clone https://github.com/your-username/flask-task-manager.git`  
`cd flask-task-manager`  
`docker compose up --build -d`  

בדיקת בריאות:  
`curl http://localhost:5000/health`  

כניסה לדפדפן:  
`http://localhost:5000/`  

---

## ☸️ פרישה ל-Kubernetes / Killercoda  

עברתי לבראנץ' **add-k8s-files** לצורך הוספת כל קבצי Kubernetes.  
כל הקבצים לפרישה נמצאים בתיקיית **k8s/**:  

- namespace.yaml  
- flask-configmap.yaml  
- flask-deployment.yaml  
- flask-service.yaml  
- mysql-deployment.yaml  
- mysql-pvc.yaml  
- mysql-secret.yaml  
- mysql-service.yaml  

להרצה בסביבת Kubernetes:  
`kubectl apply -f k8s/`  

בדיקת השירותים:  
`kubectl get svc -n flask-task`  

---

## 🔄 תהליך CI/CD  

הוגדר **צינור CI/CD** באמצעות **GitHub Actions**, הכולל שלבים:  

1. **Build** – בניית האפליקציה ובדיקת התקנות  
2. **Lint/Test** – בדיקות אוטומטיות  
3. **Docker Build** – בניית Docker Image  
4. **Push to DockerHub** – העלאת התמונה ל־DockerHub  
5. **Deploy** – פריסה אוטומטית לסביבת Kubernetes  
6. **Verify** – בדיקת Health Check אחרי פריסה  

📸 **צילומי מסך**:  
- תהליך ה־CI/CD בגיטהאב – כל השלבים ירוקים  
- האפליקציה רצה בדפדפן ומציגה רשימת משימות  
- בדיקה ב־kubectl שה־StatefulSet פעיל והנתונים נשמרים  

---

## 🧩 שימוש ב-AI  

במהלך פיתוח הפרויקט נעזרתי בכלים מבוססי **AI** לשיפור הקוד, יצירת קבצי Kubernetes, כתיבת CI/CD וכתיבת README מקצועי.  

---

## 📝 Reflection  

- למדתי איך משלבים בין **Flask**, **MySQL**, **Docker**, **Kubernetes** ו־**CI/CD** בפרויקט אחד מלא.  
- ההתמודדות העיקרית הייתה בהבנת **Persistent Volumes** ב־Kubernetes כדי להבטיח שהנתונים במסד לא נמחקים לאחר Restart.  
- הפעלת **Health Check** הייתה חשובה לוודא שהאפליקציה באמת תקינה.  
- הפרויקט המחיש איך כלי DevOps עוזרים לבנות **תהליך עבודה מסודר** – מהפיתוח ועד לפריסה אמיתית.  

---

## 📂 מבנה הפרויקט  

```
flask-task-manager/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml
├── k8s/
│   ├── namespace.yaml
│   ├── flask-configmap.yaml
│   ├── flask-deployment.yaml
│   ├── flask-service.yaml
│   ├── mysql-deployment.yaml
│   ├── mysql-pvc.yaml
│   ├── mysql-secret.yaml
│   └── mysql-service.yaml
└── .github/workflows/
    └── ci-cd.yaml
```

---

## ✅ סיכום  

פרויקט **Flask Task Manager** הוא מימוש מלא של אפליקציה מבוססת Flask עם DB, כולל סביבה מקומית עם Docker, פרישה ב־Kubernetes, ותהליך CI/CD אוטומטי מלא.  
