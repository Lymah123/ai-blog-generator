# 🤖 AI Blog Generator

> A powerful, production-ready AI-powered blog content generator built with FastAPI, React, and Hugging Face Transformers. Generate SEO-optimized blog posts in seconds with advanced NLP capabilities.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![AI Blog Generator Demo](./frontend/src/assets/demo.png)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Functionality

- 🎯 **AI-Powered Content Generation** - Leverages Hugging Face's Llama 3.3 70B model for high quality blog generation.
- 📊 **SEO Optimization** - Automatic SEO scoring and keyword integration
- 🎨 **Multiple Writing Tones** - Professional, Casual, Technical, and Educational styles.
- 📏 **Flexible Content Length** - Short (600-800), Medium (1000-1500), and Long (1800-2500).
- 💾 **Persistent Storage** - PostgreSQL database for blog history and management.
- 📱 **Responsive Design** - Beautiful UI that works on all devices.

### Advanced Features

- ⚡ **Real-time Generation** - Stream content as it's generated.
- 📈 **Analytics Dashboard** - Track word counts, SEO scores, and performance metrics.
- 📋 **Export Options** - Download blogs as Markdown files or copy to clipboard. 
- 🗂️ **Blog Management** - View, search, and manage generated content.
- 🔄 **Keyword Optimization** - Natural keyword integration for better SEO
- 🎯 **Content Post-Processing** - Automatic formatting, cleanup, and structuring.

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast Python web framework
- **AI/NLP**: [Hugging Face Transformers](https://huggingface.co/) - State-of-the-art NLP models
- **Database**: [PostgreSQL](https://www.postgresql.org/) - Reliable relational database
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
- **Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation using Python type hints

### Frontend
- **Framework**: [React 18](https://reactjs.org/) - UI library for building interfaces
- **Build Tool**: [Vite](https://vitejs.dev/) - Next-generation frontend tooling
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- **HTTP Client**: [Axios](https://axios-http.com/) - Promise-based HTTP client
- **Icons**: [Lucide React](https://lucide.dev/) - Beautiful, consistent icons
- **Markdown**: [React Markdown](https://github.com/remarkjs/react-markdown) - Markdown renderer

### DevOps & Deployment
- **Backend Hosting**: [Railway](https://railway.app/) - Modern infrastructure platform
- **Frontend Hosting**: [Vercel](https://vercel.com/) - Frontend deployment platform
- **Version Control**: Git & GitHub

## 🏗️ Architecture
```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │         │                  │         │                 │
│  React Frontend │◄───────►│  FastAPI Backend │◄───────►│   PostgreSQL    │
│   (Vite + TW)   │         │   (Python 3.11)  │         │    Database     │
│                 │         │                  │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     │
                                     ▼
                            ┌──────────────────┐
                            │  Hugging Face    │
                            │  Inference API   │
                            │  (Llama 3.3 70B) │
                            └──────────────────┘
```

### Data Flow

1. **User Input** → Frontend form submission
2. **API Request** → Backend receives blog generation parameters
3. **Prompt Building** → AI service constructs optimized prompt
4. **AI Generation** → Hugging Face API generates content
5. **Post-Processing** → Content cleanup, formatting, SEO analysis
6. **Database Storage** → Blog saved to PostgreSQL
7. **Response** → Formatted blog returned to frontend

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- Node.js 18+ and npm
- PostgreSQL 14+
- Hugging Face API key ([Get one here](https://huggingface.co/settings/tokens))

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/Lymah123/ai-blog-generator.git

cd ai-blog-generator

# Set up a Python virtual environment
cd backend
python -m venv venv

# Activate Virtual environment
# Windows
venv\Scripts\activate
# MacOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Configure environment variables
# Edit .env with your settings:
# - DATABASE_URL=postgresql://user:password@localhost:5432/bloggen
# - HUGGINGFACE_API_KEY=your_key_here
# - HUGGINGFACE_MODEL=meta-llama/Llama-3.3-70B-Instruct

# Run database migrations (tables will be created automatically)
# Start the server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Configure API URL
# Edit .env:
# VITE_API_URL=http://localhost:8000

# Start development server
npm run dev
```

### Database Setup
```bash
# Create PostgreSQL database
psql -U postgres

# In psql:
CREATE DATABASE bloggen;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE bloggen TO your_user;
\q
```

## 🚀 Usage

### Starting the Application
1. **Start Backend** (Terminal 1):
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

2. **Start Frontend** (Terminal 2):
```bash
cd frontend
npm run dev
```

3. **Access Application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Deployment URLs
- API Root: https://ai-blog-generator-production-bd0c.up.railway.app/
- API Docs: https://ai-blog-generator-production-bd0c.up.railway.app/docs
- Production: https://frontend-2t151l0f1-lymahs-projects.vercel.app
- Alias: https://frontend-ochre-rho-71.vercel.app


### Generating Your First Blog

1. Enter a blog topic (e.g., "The Future of Artificial Intelligence")
2. Select writing tone (Professional, Casual, Technical, Educational)
3. Choose content length (Short, Medium, Long)
4. Add optional keywords for SEO optimization
5. Click "Generate Blog Post"
6. Wait 20-40 seconds for AI generation
7. View, copy, or download your blog!

### API Examples

**Generate Blog Post**:
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Benefits of Cloud Computing",
    "tone": "professional",
    "length": "medium",
    "keywords": "scalability, cost-efficiency, security"
  }'
```

**Get All Blogs**:
```bash
curl "http://localhost:8000/api/v1/blogs"
```

**Get Specific Blog**:
```bash
curl "http://localhost:8000/api/v1/blogs/1"
```

**Delete Blog**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/blogs/1"
```

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/generate` | Generate new blog post |
| GET | `/api/v1/blogs` | List all blog posts |
| GET | `/api/v1/blogs/{id}` | Get specific blog post |
| DELETE | `/api/v1/blogs/{id}` | Delete blog post |
| GET | `/health` | Health check endpoint |

### Request/Response Examples

**POST /api/v1/generate**

Request:
```json
{
  "topic": "Artificial Intelligence in Healthcare",
  "tone": "professional",
  "length": "medium",
  "keywords": "AI, machine learning, diagnostics"
}
```

Response:
```json
{
  "id": 1,
  "topic": "Artificial Intelligence in Healthcare",
  "tone": "professional",
  "length": "medium",
  "keywords": "AI, machine learning, diagnostics",
  "title": "Revolutionizing Healthcare: The Impact of AI",
  "content": "# Revolutionizing Healthcare...",
  "seo_score": 85.5,
  "word_count": 1247,
  "created_at": "2026-01-06T12:00:00Z"
}
```

Full API documentation available at: http://localhost:8000/docs

## 🌐 Deployment

### Deploy Backend to Railway

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Login and Initialize**:
```bash
railway login
railway init
```

3. **Add PostgreSQL**:
```bash
railway add postgresql
```

4. **Set Environment Variables**:
```bash
railway variables set HUGGINGFACE_API_KEY=your_key
railway variables set HUGGINGFACE_MODEL=meta-llama/Llama-3.3-70B-Instruct
railway variables set ENVIRONMENT=production
```

5. **Deploy**:
```bash
cd backend
railway up
```

### Deploy Frontend to Vercel

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Deploy**:
```bash
cd frontend
vercel
```

3. **Set Environment Variable**:
   - Go to Vercel Dashboard → Settings → Environment Variables
   - Add `VITE_API_URL` with your Railway backend URL

4. **Redeploy**:
```bash
vercel --prod
```

### Environment Variables

**Backend (.env)**:
```env
DATABASE_URL=postgresql://user:password@host:port/database
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
HUGGINGFACE_MODEL=meta-llama/Llama-3.3-70B-Instruct
CORS_ORIGINS=https://yourdomain.vercel.app
ENVIRONMENT=production
```

**Frontend (.env)**:
```env
VITE_API_URL=https://your-backend.railway.app
```

## 📁 Project Structure

```
ai-blog-generator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry
│   │   ├── config.py               # Configuration management
│   │   ├── database.py             # Database connection
│   │   ├── models/
│   │   │   └── blog.py             # SQLAlchemy models
│   │   ├── schemas/
│   │   │   └── blog.py             # Pydantic schemas
│   │   ├── api/
│   │   │   └── routes.py           # API endpoints
│   │   ├── services/
│   │   │   ├── ai_service.py       # Hugging Face integration
│   │   │   └── seo_service.py      # SEO scoring logic
│   │   └── utils/
│   │       └── post_processor.py   # Content processing
│   ├── requirements.txt
│   ├── .env.example
│   └── railway.json
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── BlogForm.jsx        # Blog generation form
│   │   │   ├── BlogDisplay.jsx     # Blog content display
│   │   │   └── BlogHistory.jsx     # Blog history list
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   ├── utils/
│   │   │   └── helpers.js          # Utility functions
│   │   ├── App.jsx                 # Main application
│   │   ├── main.jsx                # React entry point
│   │   └── index.css               # Tailwind styles
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env.example
│
└── README.md
```
## 🎯 Key Features Breakdown

### 1. AI Service (`ai_service.py`)
- Integrates with Hugging Face Inference API
- Builds optimized prompts for different tones and lengths
- Handles API retries and error cases
- Processes raw AI output into structured content

### 2. SEO Service (`seo_service.py`)
- Calculates SEO scores based on multiple factors:
  - Word count optimization (800-2500 words)
  - Heading structure (H1, H2, H3 tags)
  - Keyword density and placement
  - Title optimization (40-70 characters)
  - Content structure (intro, body, conclusion)

### 3. Post Processor (`post_processor.py`)
- Cleans and formats generated content
- Extracts titles from content
- Removes artifacts and incomplete sentences
- Adds proper markdown formatting
- Counts words accurately

### 4. Frontend Components
- **BlogForm**: Interactive form with validation
- **BlogDisplay**: Renders markdown with syntax highlighting
- **BlogHistory**: Paginated list with search and filters

## 🔧 Configuration

### Backend Configuration (`config.py`)
```python
DATABASE_URL: PostgreSQL connection string
HUGGINGFACE_API_KEY: Your HF API key
HUGGINGFACE_MODEL: Model to use for generation
CORS_ORIGINS: Allowed frontend origins
ENVIRONMENT: development/production
```
### Frontend Configuration (`.env`)
```env
VITE_API_URL: Backend API base URL
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Manual Testing Checklist
- [ ] Generate blog with all tone variations
- [ ] Generate blog with all length options
- [ ] Test with and without keywords
- [ ] Verify SEO score calculation
- [ ] Test copy to clipboard
- [ ] Test download functionality
- [ ] Test blog history pagination
- [ ] Test blog deletion
- [ ] Verify responsive design

## 🐛 Troubleshooting

### Common Issues

**1. Database Connection Error**
```bash
# Check PostgreSQL is running
psql -U postgres -l

# Verify connection string in .env
DATABASE_URL=postgresql://user:password@localhost:5432/bloggen
```

**2. Hugging Face API Errors**
```bash
# Verify API key
curl -H "Authorization: Bearer $HUGGINGFACE_API_KEY" \
  https://api-inference.huggingface.co/models/meta-llama/Llama-3.3-70B-Instruct

# Check model status (503 means loading)
```

**3. CORS Errors**
```python
# Update CORS_ORIGINS in backend .env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**4. Frontend Not Connecting to Backend**
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check VITE_API_URL in frontend .env
VITE_API_URL=http://localhost:8000
```

## 📈 Performance Optimization

- **Backend**: 
  - Connection pooling for database
  - Request timeout handling
  - Efficient query optimization
  
- **Frontend**:
  - Code splitting with React.lazy
  - Image optimization
  - Debounced search inputs

## 🔒 Security

- Environment variables for sensitive data
- SQL injection prevention via SQLAlchemy ORM
- Input validation with Pydantic
- CORS configuration for production
- Rate limiting on API endpoints (recommended)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write meaningful commit messages
- Add tests for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**LYMAH**
- GitHub: [@Lymah123](https://github.com/Lymah123)
- LinkedIn: [Halimah Odunola](https://www.linkedin.com/in/harlimat-odunola-2ab261235)
- Dev.to: [Lymah](https://dev.to/lymah)

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for providing powerful AI models
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [React](https://reactjs.org/) community for amazing tools and libraries
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework

## 📞 Support

For support, email fimihanodunola625@gmail.com or create an issue in the GitHub repository.

---

⭐ **If you find this project useful, please consider giving it a star!** ⭐

Made with ❤️ and ☕ by Lymah

---
