# Quick Start Guide

Get the AI PowerPoint Assistant running in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ and npm installed
- PostgreSQL installed and running
- PowerPoint (for testing the add-in)

## Step 1: Setup (First Time Only)

Run the setup script:

```bash
./setup.sh
```

This will:
- Create Python virtual environment
- Install all Python dependencies
- Set up the database
- Install Node.js dependencies

## Step 2: Configure Database

Make sure PostgreSQL is running. Create the database:

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE pptai;

# Exit
\q
```

Update `backend/.env` if your PostgreSQL credentials are different:
```
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/pptai
```

## Step 3: Start the Application

### Option A: Start Both Services
```bash
./run.sh
# Choose option 3
```

### Option B: Start Separately

**Terminal 1 - Backend:**
```bash
cd backend
./start.sh
```

**Terminal 2 - Frontend:**
```bash
cd frontend
./start.sh
```

## Step 4: Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Step 5: Test the App

1. Open http://localhost:5173 in your browser
2. Click "Sign Up" and create an account
3. Upload a text document
4. Generate a presentation!

## Step 6: Use in PowerPoint (Optional)

To use as a PowerPoint add-in:

### For Development/Testing:

1. **Update manifest**: Edit `frontend/manifest/manifest.xml`
   - Change URLs from `https://localhost:5173` to `http://localhost:5173` (for local dev)

2. **Sideload the add-in**:

   **Windows:**
   - Copy `frontend/manifest/manifest.xml` to:
     `C:\Users\[Username]\AppData\Local\Microsoft\Office\16.0\Wef\`
   - Restart PowerPoint
   - Go to Insert > My Add-ins > Shared Folder
   - Select "AI Presentation Assistant"

   **Mac:**
   - Copy `frontend/manifest/manifest.xml` to:
     `~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/wef/`
   - Restart PowerPoint
   - Go to Insert > Add-ins > My Add-ins
   - Select "AI Presentation Assistant"

3. **Open PowerPoint** and look for the add-in in the ribbon!

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running: `pg_isready`
- Verify database exists: `psql -l | grep pptai`
- Check Python version: `python3 --version`

### Frontend won't start
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node version: `node --version`

### Database errors
- Run `python backend/init_db.py` to recreate tables
- Check connection string in `backend/.env`

### Add-in not loading
- Make sure both backend and frontend are running
- Check browser console for errors
- Verify manifest.xml has correct URLs

## What's Working

✅ User signup and login
✅ JWT authentication
✅ Document upload (txt files)
✅ Presentation generation (stubbed AI - returns fake slides)
✅ Slide editing (stubbed AI - appends "(edited)" to content)
✅ PowerPoint integration (creates/updates slides)

## What's Stubbed

⚠️ S3 file storage (files are "uploaded" but not really stored)
⚠️ OpenAI integration (returns fake generated content)
⚠️ DOCX parsing (returns placeholder text)

## Next Steps

1. Implement real OpenAI API calls in `backend/app/services/llm.py`
2. Implement real S3 uploads in `backend/app/services/s3.py`
3. Add DOCX parsing in `backend/app/services/documents.py`
4. Improve slide formatting and styling
5. Add error handling and loading states

Happy coding! 🚀
