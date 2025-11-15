
# ClassSync — Offline (SQLite + Flask)

This build removes Supabase and runs **fully offline** with a local Python backend and SQLite.

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

### Notes
- A Nuxt plugin `plugins/api.js` exposes `this.$api` methods.
- Patched files have backups `*.bak_supabase`.
- Remove Supabase dependency when ready: `npm remove @supabase/supabase-js`
- If you used extra Supabase features (storage, RLS), add endpoints to `backend/server.py` similarly.
