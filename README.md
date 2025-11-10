# AI PowerPoint Presentation Assistant

A full-stack application that allows users to generate and edit PowerPoint presentations using AI, integrated as a PowerPoint Task Pane Add-in.

> **🚀 Want to get started quickly?** See [QUICKSTART.md](./QUICKSTART.md) for a 5-minute setup guide!

## Quick Start

```bash
# 1. Run setup (first time only)
./setup.sh

# 2. Start the application
./run.sh
```

That's it! Visit http://localhost:5173 to use the app.

---

## Architecture

- **Backend**: Python FastAPI + PostgreSQL + SQLAlchemy + JWT Auth
- **Frontend**: React + TypeScript + Vite + Office.js
- **AI Services**: OpenAI LLM (stubbed), AWS S3 (stubbed)

## Features

- User authentication (signup/login with JWT)
- Document upload (txt/docx)
- AI-powered presentation generation from documents
- Slide editing via natural language instructions
- Direct PowerPoint integration via Office.js

## Project Structure

```
ppt-ai-assistant/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── core/     # Config, database, security
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── api/      # API routes
│   │   └── services/ # Business logic
│   └── requirements.txt
└── frontend/         # React + Office.js frontend
    ├── src/
    │   ├── components/
    │   ├── api/
    │   ├── context/
    │   └── office/
    └── manifest/     # Office Add-in manifest
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:
   Create a `.env` file in the `backend` directory:
   ```env
   APP_NAME=ppt-ai-backend
   DEBUG=True
   DATABASE_URL=postgresql://user:password@localhost:5432/pptai
   JWT_SECRET_KEY=your-secret-key-change-this-in-production
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
   CORS_ALLOWED_ORIGINS=["http://localhost:5173"]

   # Optional (for future S3 integration)
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret
   AWS_S3_BUCKET_NAME=your-bucket-name

   # Optional (for future OpenAI integration)
   OPENAI_API_KEY=your-openai-key
   ```

5. **Set up PostgreSQL database**:
   ```bash
   # Create database
   createdb pptai
   ```

6. **Create database tables**:
   ```bash
   # Run Python to create tables
   python -c "from app.core.database import Base, engine; from app.models import user, organization, document, presentation; Base.metadata.create_all(bind=engine)"
   ```

7. **Run the development server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set environment variables**:
   Create a `.env` file in the `frontend` directory:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

### PowerPoint Add-in Setup (Sideloading)

To test the add-in in PowerPoint:

1. **Start both backend and frontend servers** (see above)

2. **For Windows**:
   - Open PowerPoint
   - Go to File > Options > Trust Center > Trust Center Settings > Trusted Add-in Catalogs
   - Add the path to `frontend/manifest/` as a trusted catalog
   - Check "Show in Menu"
   - Restart PowerPoint
   - Go to Insert > My Add-ins > Shared Folder
   - Select the AI Presentation Assistant add-in

3. **For Mac**:
   - Copy `frontend/manifest/manifest.xml` to:
     `/Users/{username}/Library/Containers/com.microsoft.Powerpoint/Data/Documents/wef/`
   - Restart PowerPoint
   - Go to Insert > Add-ins > My Add-ins
   - Select the AI Presentation Assistant add-in

4. **For Office Online**:
   - Upload the manifest via the Office Add-ins portal for testing

## Development Workflow

1. **User signs up/logs in** via the task pane
2. **Uploads a document** (txt or docx file)
3. **Generates presentation** by selecting document, slide count, and tone
4. **Slides are automatically created** in the current PowerPoint presentation
5. **Edits slides** by selecting slide index and providing natural language instructions
6. **Slide is updated** in the PowerPoint presentation

## API Endpoints

### Authentication
- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Login and receive JWT token

### Documents
- `POST /documents/upload` - Upload document (multipart/form-data)
- `GET /documents` - List all documents for current organization

### Presentations
- `POST /presentations/from-document` - Generate presentation from document
- `POST /presentations/{id}/slides/{index}/edit` - Edit specific slide

### Health
- `GET /health` - Health check endpoint

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy 2.0**: SQL toolkit and ORM
- **PostgreSQL**: Relational database
- **Pydantic v2**: Data validation
- **JWT**: Authentication
- **boto3**: AWS S3 client (stubbed)
- **OpenAI**: LLM integration (stubbed)

### Frontend
- **React 18**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool
- **Office.js**: PowerPoint integration
- **Axios**: HTTP client

## Current Implementation Status

### ✅ Implemented (Skeleton/Stub)
- Complete project structure
- User authentication (JWT)
- Document upload (file handling stubbed)
- Presentation generation (LLM stubbed with fake data)
- Slide editing (LLM stubbed with fake edits)
- PowerPoint integration (Office.js)
- Full API and frontend structure

### 🚧 TODO (Placeholders)
- Real S3 file upload (currently stubbed)
- Real OpenAI LLM calls (currently returns fake data)
- DOCX parsing (currently returns placeholder text)
- Advanced slide formatting
- Image handling
- Multi-organization management
- Database migrations (Alembic)

## Security Notes

- Change `JWT_SECRET_KEY` in production
- Use HTTPS in production
- Implement rate limiting
- Add input validation and sanitization
- Use environment-specific CORS settings
- Implement proper error handling

## Contributing

This is a skeleton codebase. To add real functionality:

1. **S3 Integration**: Implement `app/services/s3.py` upload function
2. **OpenAI Integration**: Implement `app/services/llm.py` with real API calls
3. **Document Parsing**: Add DOCX parsing in `app/services/documents.py`
4. **Database Migrations**: Set up Alembic for schema migrations
5. **Testing**: Add unit and integration tests
6. **Error Handling**: Improve error messages and logging

## License

MIT
