# ✅ Flask Todo App

A full-stack **Todo list application** built with **Flask**, featuring:

- User authentication (register, login, logout)  
- Task management (create, read, update, delete, toggle complete/incomplete)  
- Task priority (**high / medium / low**) and deadlines  
- Filtering by **completed / incomplete / priority / date ranges**  
- AI assistant with **local embeddings (SentenceTransformers + FAISS)** to query tasks in natural language  
- Flash messages for success & errors  
- SCSS support with **Flask-Assets** (modular, per-blueprint styles)  
- Blueprints for a clean and scalable project structure  

---

## 📂 Project Structure

```
flask_todo/
├─ app/
│  ├─ __init__.py          # App factory, blueprint registration
│  ├─ extensions.py        # Flask extensions (db, migrate, login, assets)
│  ├─ models/              # SQLAlchemy models
│  │   ├─ user.py
│  │   └─ task.py
│  ├─ auth/                # Auth blueprint
│  │   ├─ routes.py
│  │   └─ forms.py
│  ├─ todo/                # Todo blueprint
│  │   ├─ routes.py
│  ├─ ai/                  # AI assistant blueprint (RAG)
│  │   ├─ rag.py           # FAISS + SentenceTransformers
│  │   └─ routes.py        # AI chat endpoint
│  ├─ main/                # Main blueprint (homepage, base)
│  ├─ templates/           # Jinja2 templates
│  │   ├─ base.html
│  │   ├─ auth/
│  │   └─ todos/
│  └─ static/
│      ├─ scss/            # SCSS files
│      │   ├─ _variables.scss
│      │   ├─ main/main.scss
│      │   ├─ auth/auth.scss
│      │   └─ todo/todo.scss
│      └─ css/             # Compiled CSS (output)
├─ migrations/             # Alembic migrations
├─ config.py               # Config classes (Dev, Prod)
├─ wsgi.py                 # Entry point
├─ .env                    # Environment variables
├─ requirements.txt        # Python dependencies
└─ README.md
```

---

## 🚀 Features

- 🔑 **Authentication** — register/login/logout with secure password hashing  
- 📝 **Todo CRUD** — add, edit, delete, and toggle tasks  
- 🎯 **Priority & Deadline** — assign deadlines and priorities (High, Medium, Low)  
- 🔍 **Filtering** — view completed/incomplete tasks, filter by priority, or by date (today, tomorrow, this week, next week, this month)  
- 🤖 **AI Assistant** — ask natural language queries like *"Show me my incomplete tasks this week"*  
  - Powered by **SentenceTransformers + FAISS** (local embeddings, no OpenAI quota needed)  
  - Results displayed as a **styled table** inside the AI chat popup  
- 🎨 **Styling** — modular SCSS per blueprint (`auth.scss`, `todo.scss`, `main.scss`)  
- ⚡ **Flash messages** — success, error, and info feedback  
- 🗄️ **SQLite with SQLAlchemy** + migrations via Alembic  

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/flask-todo.git
cd flask-todo
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment variables (`.env`)
Create a `.env` file in the project root:
```bash
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=supersecretkey
SQLALCHEMY_DATABASE_URI=sqlite:///app.db
```

### 5. Initialize the database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the app
```bash
flask run
```

Go to 👉 http://127.0.0.1:5000/

---

## 🎨 SCSS Workflow

SCSS files live in `app/static/scss/`.  
They are compiled automatically with **Flask-Assets** into `app/static/css/`.

Bundles:
- `main.scss` → `main.min.css` (navbar, flash, global)
- `auth.scss` → `auth.min.css` (login/register pages)
- `todo.scss` → `todo.min.css` (todo list pages, AI chat styles)
- `edit.scss` → `edit.min.css` (edit task pages)

---

## 📸 Screenshots

### Landing Page
![Landing Page](docs/landing-page-ss.png)

### Login Page
![Login Page](docs/login-page-ss.png)

### Register Page
![Register Page](docs/register-page-ss.png)

### Todo List – All Tasks
![All Tasks](docs/filter-all-ss.png)

### Todo List – Completed Tasks
![Completed Tasks](docs/filter-com-ss.png)

### Todo List – Incomplete Tasks
![Incomplete Tasks](docs/filter-incom-ss.png)

### AI Chat Assistant
![AI Chat](docs/ai-chat-ss.png)

---

## 🛠 Tech Stack

- [Flask](https://flask.palletsprojects.com/) — web framework  
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM  
- [Flask-Migrate](https://flask-migrate.readthedocs.io/) — Alembic migrations  
- [Flask-Login](https://flask-login.readthedocs.io/) — session management  
- [Flask-Assets](https://flask-assets.readthedocs.io/) — SCSS/CSS bundling  
- [WTForms](https://wtforms.readthedocs.io/) — form handling  
- [SentenceTransformers](https://www.sbert.net/) — local embeddings for AI assistant  
- [FAISS](https://github.com/facebookresearch/faiss) — vector search backend  

---

## 📌 Future Improvements

- 🌙 Dark mode toggle  
- 🔍 Full-text search in tasks  
- 📱 Responsive navbar and chat UI (mobile friendly)  
- 📡 JSON API with JWT authentication  
- 📊 AI chat history stored in DB for persistence  

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.