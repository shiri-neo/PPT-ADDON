# Getting Started - PPT AI Assistant

Complete guide to get the app running in 5 minutes.

## Requirements

- **Python 3.9-3.12** (NOT 3.13 - it's too new!)
- **Node.js 18+** and npm
- That's it! No PostgreSQL or other dependencies needed

## Quick Start

### 1. Install Python 3.12 (if you have Python 3.13)

**macOS:**
```bash
brew install python@3.12
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv
```

**Windows:**
Download from https://www.python.org/downloads/release/python-3120/

### 2. Clean Previous Attempts (if any)

```bash
cd backend
rm -rf venv pptai.db __pycache__
cd ../frontend
rm -rf node_modules package-lock.json
cd ..
```

### 3. Run Setup

```bash
./setup.sh
```

This will:
- ✅ Detect compatible Python version (3.9-3.12)
- ✅ Create virtual environment
- ✅ Install all Python dependencies
- ✅ Test backend setup
- ✅ Create database (SQLite - no config needed!)
- ✅ Install Node.js dependencies

### 4. Start the App

**Option A - Interactive Menu:**
```bash
./run.sh
# Choose option 3 (start both services)
```

**Option B - Separate Terminals:**

Terminal 1 (Backend):
```bash
cd backend
./start.sh
```

Terminal 2 (Frontend):
```bash
cd frontend
./start.sh
```

### 5. Test the App

1. Open http://localhost:5173 in your browser
2. Click **"Sign Up"** tab
3. Enter:
   - Email: `test@example.com`
   - Password: `password123` (twice)
4. Click **"Sign Up"**
5. You should be automatically logged in!

## Verify It's Working

### Check Backend
Open http://localhost:8000/docs - you should see the API documentation

### Check Frontend
Open http://localhost:5173 - you should see the login/signup page

### Test Signup Flow
1. Go to http://localhost:5173
2. Sign up with any email/password
3. You'll be logged in automatically
4. Try uploading a `.txt` file
5. Generate a presentation
6. See fake AI-generated slides!

## What You Can Do

Once logged in:

1. **Upload Documents**
   - Upload `.txt` files (works)
   - Upload `.docx` files (returns placeholder for now)

2. **Generate Presentations**
   - Select uploaded document
   - Choose number of slides (1-20)
   - Pick tone (formal, casual, marketing, academic)
   - Click "Generate Presentation"
   - Get 2-3 fake AI slides (stubbed)

3. **Edit Slides**
   - Enter slide index (0, 1, 2, etc.)
   - Enter instruction (e.g., "Make it shorter")
   - Click "Apply Edit"
   - Slide gets "(edited)" appended (stubbed)

## Common Issues

### "Python 3.13 is too new"
Install Python 3.12:
```bash
brew install python@3.12
```
Then run `./setup.sh` again

### "Module not found" errors
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Signup button does nothing
1. Check browser console (F12) for errors
2. Make sure backend is running at http://localhost:8000
3. Test backend: `curl http://localhost:8000/health`

### Port already in use
```bash
# Kill backend (port 8000)
lsof -ti:8000 | xargs kill -9

# Kill frontend (port 5173)
lsof -ti:5173 | xargs kill -9
```

## PowerPoint Add-in (Optional)

To test in PowerPoint:

1. Make sure both backend and frontend are running
2. Find the manifest file: `frontend/manifest/manifest.xml`

**macOS:**
```bash
# Copy manifest
cp frontend/manifest/manifest.xml ~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/wef/

# Restart PowerPoint
# Go to: Insert > Add-ins > My Add-ins
# Select "AI Presentation Assistant"
```

**Windows:**
```bash
# Copy manifest to:
# C:\Users\<username>\AppData\Local\Microsoft\Office\16.0\Wef\

# Restart PowerPoint
# Go to: Insert > My Add-ins > Shared Folder
# Select "AI Presentation Assistant"
```

## Technology Stack

**Backend:**
- FastAPI (Python web framework)
- SQLite (zero-config database)
- SQLAlchemy (ORM)
- PyJWT (authentication)
- Passlib (password hashing)

**Frontend:**
- React 18
- TypeScript
- Vite (build tool)
- Office.js (PowerPoint integration)
- Axios (HTTP client)

## What's Real vs Stubbed

### ✅ Real and Working:
- User signup/login
- JWT authentication
- Document upload
- SQLite database
- PowerPoint integration
- Slide creation/editing in PowerPoint

### ⚠️ Stubbed (Fake Data):
- AI slide generation (returns hardcoded slides)
- AI slide editing (appends "(edited)" to content)
- S3 file storage (files processed but not stored)
- DOCX parsing (returns placeholder text)

## Next Steps

Want to add real AI?

1. **OpenAI Integration**: Edit `backend/app/services/llm.py`
2. **S3 Storage**: Edit `backend/app/services/s3.py`
3. **DOCX Parsing**: Install `python-docx` and update `backend/app/services/documents.py`

## Need Help?

- Check `TROUBLESHOOTING.md` for common issues
- Run backend tests: `cd backend && source venv/bin/activate && python test_setup.py`
- Check API docs: http://localhost:8000/docs
- Check browser console: F12 in your browser

---

**Happy coding!** 🚀
