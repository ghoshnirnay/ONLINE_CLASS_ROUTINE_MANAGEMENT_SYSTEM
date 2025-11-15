# classsync
Software_engineering_project


# ClassSync — Offline (SQLite + Flask)



## Backend (Windows PowerShell)

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python setup_db.py
python server.py
```

API base: `http://127.0.0.1:5000/api`

## Frontend (Nuxt 2)

```
npm install
$env:API_BASE='http://127.0.0.1:5000/api'; npm run dev
```
