# Full-stack Job Search Automation Platform

A comprehensive job search automation platform with a FastAPI backend and React UI. It scrapes job boards, ranks roles by skills and keywords, generates tailored resumes via AI, stores data in SQL, and includes user authentication and scheduling.

## Features

- 🔐 **User Authentication**: JWT-based secure authentication
- 🔍 **Job Scraping**: Automated job board scraping (mock data for demo)
- 📊 **Job Ranking**: Intelligent ranking based on user skills and keywords
- 📝 **AI Resume Generation**: Generate tailored resumes using OpenAI (or template-based fallback)
- 💾 **SQL Database**: SQLite with async SQLAlchemy for data persistence
- ⏰ **Scheduling**: Automated job search scheduling with APScheduler
- 🎨 **Modern React UI**: Responsive dashboard with TypeScript

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   │   └── routes/       # Route handlers
│   │   ├── core/             # Configuration and security
│   │   ├── db/               # Database setup
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── tests/            # Test files
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── context/          # React context (Auth)
│   │   ├── pages/            # Page components
│   │   └── services/         # API services
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The UI will be available at `http://localhost:3000`.

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login (OAuth2 form)
- `POST /api/v1/auth/login/json` - Login (JSON body)

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user

### Jobs
- `POST /api/v1/jobs/search` - Search and scrape jobs
- `GET /api/v1/jobs` - Get all jobs
- `GET /api/v1/jobs/{id}` - Get specific job
- `PATCH /api/v1/jobs/{id}` - Update job status
- `DELETE /api/v1/jobs/{id}` - Delete job

### Resumes
- `POST /api/v1/resumes/generate` - Generate AI resume
- `GET /api/v1/resumes` - Get all resumes
- `GET /api/v1/resumes/{id}` - Get specific resume
- `PUT /api/v1/resumes/{id}` - Update resume
- `DELETE /api/v1/resumes/{id}` - Delete resume

### Schedules
- `POST /api/v1/schedules` - Create schedule
- `GET /api/v1/schedules` - Get all schedules
- `GET /api/v1/schedules/{id}` - Get specific schedule
- `PUT /api/v1/schedules/{id}` - Update schedule
- `DELETE /api/v1/schedules/{id}` - Delete schedule
- `POST /api/v1/schedules/{id}/activate` - Activate schedule
- `POST /api/v1/schedules/{id}/deactivate` - Deactivate schedule

## Configuration

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite+aiosqlite:///./job_search.db
OPENAI_API_KEY=your-openai-api-key  # Optional, for AI resume generation
```

## Running Tests

```bash
cd backend
PYTHONPATH=. pytest app/tests/ -v
```

## Tech Stack

### Backend
- FastAPI - Modern Python web framework
- SQLAlchemy 2.0 - Async ORM
- Pydantic - Data validation
- JWT - Authentication
- APScheduler - Job scheduling
- BeautifulSoup4 - Web scraping
- OpenAI - AI resume generation

### Frontend
- React 18 - UI framework
- TypeScript - Type safety
- Vite - Build tool
- React Router - Navigation
- Axios - HTTP client

## License

MIT License - see LICENSE file for details