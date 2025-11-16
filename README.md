# PPT AI Assistant

AI-powered PowerPoint presentation generator using GPT-4 for content creation and DALL-E 3 for custom slide images.

## 🚀 Features

### AI-Powered Generation
- **GPT-4 Turbo** analyzes your documents and generates engaging, personalized content
- **DALL-E 3** creates unique, relevant images for each slide (1792x1024 widescreen)
- **Custom instructions** support - AI strictly follows your specific requirements  
- **Company branding** - Automatic integration of your colors, fonts, and logo
- **Multiple tones** - Formal, casual, marketing, or academic

### Two Deployment Modes

#### 1. 🌐 **Web Application** (Management & Admin)
Full-featured web dashboard for user management, document library, and analytics.

#### 2. 📊 **PowerPoint Add-in** (Streamlined Creation)
Integrated directly into PowerPoint for quick generation and editing.

## 📋 Quick Start

### Prerequisites
- **Python 3.11 or 3.12** (Python 3.13 not yet supported due to library compatibility)
- Node.js 16+
- OpenAI API key

### Backend
\`\`\`bash
cd backend
python3.12 -m venv venv  # Use Python 3.11 or 3.12, NOT 3.13
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add OPENAI_API_KEY=sk-your-key-here
./start.sh
\`\`\`

### Frontend
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

Access at http://localhost:5173

## 🎨 How It Works

1. **Upload** a document (.txt, .docx, .pdf, .pptx)
2. **GPT-4** analyzes content and extracts key points
3. **DALL-E** generates unique images for each slide
4. **Download** or apply directly to PowerPoint

## 🔑 Configuration

Set in `backend/.env`:
\`\`\`
OPENAI_API_KEY=sk-your-actual-key-here
\`\`\`

Without API key: Falls back to stub responses (no AI features).

See full documentation in this README for detailed setup and usage.
