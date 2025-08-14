# Base image עם Python 3.11
FROM python:3.11-slim

# הגדרת working directory
WORKDIR /app

# העתקת קובץ requirements והתקנת התלויות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קוד האפליקציה והטמפלטים
COPY app.py .
COPY templates/ ./templates/

# הגדרת משתני סביבה עבור MySQL
ENV MYSQL_HOST=mysql_db
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=mypassword
ENV MYSQL_DATABASE=task_manager

# חשיפת הפורט שבו Flask ירוץ
EXPOSE 5000

# פקודת הרצה
CMD ["python3", "app.py"]

