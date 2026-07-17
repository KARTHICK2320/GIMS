# GIMS — Grocery Inventory Management System

A full-stack inventory management system for grocery retail, built with a React.js frontend and a Flask (Python) REST API backend. Supports real-time stock tracking, role-based access via JWT authentication, and category-wise inventory management across multiple departments.

## 🧱 Tech Stack

### Frontend
- **React.js** (Vite)
- **JavaScript** (ES6+)
- **Plain CSS** / CSS Modules
- **React Context API** (state management)

### Backend
- **Python**
- **Flask**
- **SQLite** (via built-in `sqlite3` — raw SQL queries with auto-seeding)
- **PyJWT** — manual JWT authentication & protected routes
- **MVC-style architecture**

---

## ✨ Features

- **Multi-department inventory** — Grocery, Beverages, Dairy, Fruits & Vegetables, Bakery, and Household categories
- **Full CRUD operations** via modal-based forms for adding, editing, and removing inventory items
- **Search and filtering** across inventory items
- **Authentication** — Manual JWT-based login (PyJWT) with protected API routes
- **REST API integration** between frontend and backend with defined API contracts
- **Role-based data access** for inventory operations (Admin vs. User)
- **Dashboard view** for real-time stock overview
- **Alerts module** for inventory-related notifications
- **Reports module** for inventory summaries

---

## 📁 Project Structure

```text
GIMS/
├── frontend/          # React.js + Vite application
│   ├── src/
│   ├── package.json
│   └── ...
├── backend/           # Flask (Python) REST API
│   ├── app.py         # Entry point
│   ├── requirements.txt
│   ├── .env.example
│   └── ...            # MVC-style: routes, models, controllers
└── README.md          # Project documentation
```

---

## ⚙️ Getting Started

### Prerequisites
- **Python 3.9+** recommended
- **Node.js (v18+ recommended)** — for the frontend
- **pip** and **npm**

### 1. Clone the repository
```bash
git clone https://github.com/KARTHICK2320/GIMS.git
cd GIMS
```

### 2. Backend setup

Change directory to `backend`:
```bash
cd backend
```

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

Install dependencies:
```bash
pip install -r requirements.txt
```

Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
*(On Windows PowerShell, use `copy .env.example .env` if `cp` is unavailable).*

Configure your environment variables in `.env`. The project runs out-of-the-box using a local SQLite database (`gims.db`), so you only need to make sure `JWT_SECRET` is set:
```ini
PORT=5000
FLASK_ENV=development
JWT_SECRET=your_jwt_secret_key_here
CORS_ORIGIN=http://localhost:3000
```

Start the Flask server:
```bash
python app.py
```
> [!NOTE]
> The SQLite database file (`gims.db`) is automatically created and seeded with default categories and products on your very first run!

By default, the backend Flask server runs on [http://localhost:5000](http://localhost:5000).

### 3. Frontend setup

In a separate terminal window:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the frontend development server:
```bash
npm run dev
```

The frontend will start on Vite's default port (typically [http://localhost:3000](http://localhost:3000) or [http://localhost:5173](http://localhost:5173)). Make sure the port matches the `CORS_ORIGIN` set in your backend's `.env` configuration.

---

## 🔐 Environment Variables

This project uses a `.env` file in `/backend` for configuration (e.g. server port, JWT secret). Never commit your real `.env` file to version control — only `.env.example` should be tracked. The actual `.env` and the virtual environment folder (`venv/`) are excluded via `.gitignore`.

---

## 🗺️ Roadmap / Possible Improvements

- [ ] Deployment (e.g., Vercel/Netlify for the frontend, Render/Railway for the Flask backend)
- [ ] Automated testing
- [ ] Pagination for large inventory datasets
- [ ] Chart-based analytics on the dashboard

---

## 👤 Author

**Karthickraja K**

- GitHub: [@KARTHICK2320](https://github.com/KARTHICK2320)
- LinkedIn: [karthickraja-k23](https://linkedin.com/in/karthickraja-k23)
- Email: karthickr2304@gmail.com

---
