# GIMS Backend - Deployment & Configuration Guide

This guide describes how to configure, set up, and deploy the GIMS (Grocery Inventory Management System) Python Flask + MySQL backend.

---

## 💻 Local Setup Instructions

1. **Prerequisites**: Ensure you have Python (version 3.10+) and MySQL Server installed.
2. **Clone/Navigate**: Navigate to the `gims-backend-flask` folder.
3. **Environment**:
   - Create a virtual environment: `py -m venv venv`
   - Activate it: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. **Dependencies**: Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. **Database Migration**:
   - Run the SQL queries inside `database/schema.sql` (found in the original Node folder or copy it over) in your local MySQL instance.
6. **Environment Variables**:
   - Copy `.env.example` to `.env`
   - Fill in your local MySQL root password, user, database name, and define a custom `JWT_SECRET`.
7. **Run Server**: Run the development server:
   ```bash
   python app.py
   ```
   The backend will connect, test its pool connection, and start listening on [http://localhost:5000](http://localhost:5000).

---

## ☁️ Production Deployment

### Option A: Railway (Recommended for MySQL + Flask)
Railway is highly recommended because you can spin up a managed MySQL database and a Flask app side-by-side easily.

1. **Create MySQL Service**:
   - Log into Railway and select **New Project -> Provision MySQL**.
   - Copy the connection URL variables provided by Railway (`MYSQLHOST`, `MYSQLPORT`, `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE`).
2. **Deploy Flask Backend**:
   - Select **New Project -> Deploy from GitHub** and connect your repository.
   - Under **Variables** in your Flask service settings, add the required environmental variables:
     - `PORT` = `8080` (Railway will bind to this automatically)
     - `FLASK_ENV` = `production`
     - `DB_HOST` = `${{MYSQLHOST}}` (References the provisioned database service)
     - `DB_PORT` = `${{MYSQLPORT}}`
     - `DB_USER` = `${{MYSQLUSER}}`
     - `DB_PASSWORD` = `${{MYSQLPASSWORD}}`
     - `DB_NAME` = `${{MYSQLDATABASE}}`
     - `JWT_SECRET` = `[A_LONG_RANDOM_SECURE_PHRASE]`
     - `JWT_EXPIRES_IN` = `86400`
     - `CORS_ORIGIN` = `[URL_OF_YOUR_DEPLOYED_REACT_FRONTEND]`
3. **Build Command**:
   - Railway will automatically detect the `Procfile` and use `gunicorn` to start the server. Make sure `gunicorn` is listed in your deployment dependencies (we've included it in the `requirements.txt`).
4. **Database Import**:
   - Connect to the Railway MySQL instance using your favorite SQL client (e.g. DBeaver or MySQL Workbench) and load the `schema.sql` queries to build the tables.

---

### Option B: Render
Render is another great platform offering static site and web service hosting.

1. **Deploy MySQL Database**:
   - Render does not offer built-in MySQL databases on their free tier, so you must spin up a MySQL database via a service provider (like Aiven, Clever Cloud, or PlanetScale), or use a paid Render PostgreSQL database (requires minor adjustments to database models).
2. **Deploy Flask Backend**:
   - In Render, click **New -> Web Service**.
   - Connect your GitHub repository.
   - Set the runtime to **Python 3**.
   - Set the Build Command: `pip install -r requirements.txt`
   - Set the Start Command: `gunicorn "app:create_app()"`
   - Click **Advanced** and set the required environment variables matching the `.env.example` file.
