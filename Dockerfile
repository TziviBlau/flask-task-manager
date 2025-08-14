# שלב 1 - בחירת תמונת בסיס
FROM python:3.10-slim

# שלב 2 - הגדרת תיקיית עבודה
WORKDIR /app

# שלב 3 - העתקת קבצי הדרישות
COPY requirements.txt .

# שלב 4 - התקנת חבילות
RUN pip install --no-cache-dir -r requirements.txt

# שלב 5 - העתקת קבצי הפרויקט
COPY . .

# שלב 6 - הפעלת האפליקציה
CMD ["python", "app.py"]
