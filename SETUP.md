# 🚀 Quick Setup Guide

Follow these steps to get your PPT AI Assistant running:

## Prerequisites

- **Python 3.11 or 3.12** (NOT Python 3.13 - it has compatibility issues)
- Node.js 16+
- OpenAI API key

## Step 1: Backend Setup

```bash
cd backend

# Create virtual environment with Python 3.12 (if not exists)
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI API key to .env file (line 14)
# OPENAI_API_KEY=sk-your-actual-key-here

# Start the backend
./start.sh
```

The backend should start at **http://localhost:8000**

You should see:
```
✅ Backend ready!
🌐 Starting server at http://localhost:8000
```

## Step 2: Frontend Setup

In a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend should start at **http://localhost:5173**

## Step 3: Access the App

1. Open browser: **http://localhost:5173**
2. You should see a signup/login screen
3. Create an account:
   - Email: test@example.com
   - Password: password123
   - Organization: My Company
4. Start using the app!

## 🐛 Troubleshooting

### Black Screen / Infinite Loading

**Fixed!** The app was waiting too long for Office.js. Now it has a 2-second timeout.

Just refresh your browser: **http://localhost:5173**

### Backend Won't Start

Check if dependencies are installed:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "timeout of 10000ms exceeded"

The backend isn't running. Make sure backend started successfully on port 8000.

### OpenAI API Not Working

1. Check your API key in `backend/.env` line 14
2. Restart backend after adding the key
3. You should see: `⚠️ WARNING: OpenAI API key not configured!` OR `✅ OpenAI client initialized`

## ✅ You're Ready!

Once both servers are running and you've signed up, you can:

- Upload documents
- Generate AI-powered presentations
- Configure company branding
- Download PPTX files

Enjoy! 🎉
