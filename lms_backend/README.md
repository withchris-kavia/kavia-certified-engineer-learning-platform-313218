# LMS Backend (FastAPI)

## Endpoints
- Health: `GET /health`, `/ready`, `/live`
- Auth: `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me`
- Courses: `GET /api/courses`, `GET /api/courses/{course_id}`
- Lessons: `GET /api/lessons/{lesson_id}`
- Enrollments: `POST /api/enrollments`, `GET /api/enrollments/me`
- Progress: `GET /api/progress/me`, `POST /api/progress`
- Assessments: `GET /api/assessments/{lesson_id}`, `POST /api/assessments/{lesson_id}/submit`

## Environment variables
See `.env.example`. The orchestrator should provide real values in `.env`, especially:
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `CORS_ORIGINS`

## Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 3001
```

## Notes
This scaffold auto-creates tables on startup. For production, use Alembic migrations.
