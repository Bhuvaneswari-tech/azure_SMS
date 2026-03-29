# Student Management System - FastAPI

## Project Structure

- app/
  - main.py
  - models/
    - database.py
    - models.py
  - schemas/
    - schemas.py
  - repositories/
    - repository.py
  - services/
    - service.py
  - controllers/
    - student_controller.py
    - course_controller.py
- alembic/
  - env.py
  - versions/
- alembic.ini
- requirements.txt

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run Alembic migrations:
   ```bash
   alembic revision --autogenerate -m "init"
   alembic upgrade head
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints
- `/api/students/` - CRUD for students
- `/api/courses/` - CRUD for courses
