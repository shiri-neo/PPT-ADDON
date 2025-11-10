# Troubleshooting Guide

## Python 3.13 Issue (pydantic-core build fails)

**Problem:** You see error `Failed building wheel for pydantic-core` when running setup.

**Cause:** Python 3.13 is too new. Pydantic doesn't support it yet.

**Solution:** Install Python 3.12 or 3.11

### macOS:
```bash
# Install Python 3.12
brew install python@3.12

# Remove old virtual environment
cd backend
rm -rf venv
cd ..

# Run setup again
./setup.sh
```

### Linux (Ubuntu/Debian):
```bash
# Install Python 3.12
sudo apt update
sudo apt install python3.12 python3.12-venv

# Remove old virtual environment
cd backend
rm -rf venv
cd ..

# Run setup again
./setup.sh
```

### Windows:
1. Download Python 3.12 from https://www.python.org/downloads/
2. Install it
3. Delete the `backend/venv` folder
4. Run `setup.sh` again

---

## Can't Sign Up / Frontend Not Working

**Problem:** Signup button doesn't work or shows errors

**Possible causes:**

### 1. Backend not running
```bash
# Check if backend is running at http://localhost:8000
curl http://localhost:8000/health

# If you get "connection refused", start backend:
cd backend
./start.sh
```

### 2. CORS issues
Check browser console (F12). If you see CORS errors:

Edit `backend/.env` and ensure:
```
CORS_ALLOWED_ORIGINS=["http://localhost:5173","https://localhost:5173"]
```

### 3. Database not initialized
```bash
cd backend
source venv/bin/activate
python init_db.py
```

---

## SQLite Database Issues

**Problem:** Database errors or "no such table" errors

**Solution:**
```bash
# Remove database and recreate
cd backend
rm pptai.db
source venv/bin/activate
python init_db.py
```

---

## Port Already in Use

**Problem:** `Address already in use` error

**Solution:**

### Backend (port 8000):
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend (port 5173):
```bash
# macOS/Linux
lsof -ti:5173 | xargs kill -9

# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

---

## Node Module Issues

**Problem:** Frontend won't start or shows module errors

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Starting Fresh

If nothing works, start completely fresh:

```bash
# Clean everything
cd backend
rm -rf venv pptai.db __pycache__
cd ../frontend
rm -rf node_modules package-lock.json
cd ..

# Run setup again
./setup.sh
```

---

## Check Versions

Run these to verify your environment:

```bash
# Python version (should be 3.9-3.12)
python3 --version

# Node version (should be 18+)
node --version

# npm version
npm --version
```

---

## Still Having Issues?

1. Check backend logs in terminal where `./start.sh` is running
2. Check browser console (F12) for frontend errors
3. Check that both services are running:
   - Backend: http://localhost:8000/docs
   - Frontend: http://localhost:5173

4. Try accessing API directly:
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"ok"}
   ```
