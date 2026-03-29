Student Management System - FastAPI
===================================

Overview
--------
This project is a Student Management System built using FastAPI, SQLAlchemy, and Alembic. It demonstrates a modular structure with models, schemas, repositories, services, and controllers for managing students and courses.

Project Structure
-----------------
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

Setup Instructions
------------------
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Alembic (if not already present):**
   ```bash
   alembic init alembic
   ```
   (This creates the alembic/ folder and alembic.ini. Already included in this project.)

3. **Configure Alembic:**
   - In `alembic.ini`, set the `sqlalchemy.url` to match your database (default is SQLite: `sqlite:///./student.db`).
   - In `alembic/env.py`, ensure your models are imported and `target_metadata` is set to `Base.metadata` from your models.

4. **Create a migration revision:**
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```
   This generates a migration script in `alembic/versions/`.

5. **Apply migrations to the database:**
   ```bash
   alembic upgrade head
   ```

6. **Run the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

Webhook Endpoint
----------------
The project includes a webhook endpoint at `/webhook` that accepts POST requests with a JSON payload.

**To test the webhook:**
```bash
curl -X POST "http://127.0.0.1:8000/webhook" -H "Content-Type: application/json" -d '{"test": "data"}'
```
You should receive a response with the status and the payload you sent.

API Endpoints
-------------
- `/api/students/` - CRUD operations for students
- `/api/courses/` - CRUD operations for courses

Notes
-----
- Make sure to run migrations after modifying models.
- Use the service and repository layers for business logic and database access.
- Controllers (routers) handle API endpoints and dependency injection.

For more details, see the README.md in the project root.

To apply the migration to your database
alembic upgrade head

Sample API Usage (Step-by-Step)
------------------------------

1. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Obtain a JWT token (login):**
   - Use the `/api/token` endpoint with username and password (form data).
   - Example using `curl`:
     ```bash
     curl -X POST "http://127.0.0.1:8000/api/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin@example.com&password=adminpass"
     ```
   - The response will include an `access_token`.

3. **Create a new student:**
   - Use the `/api/students/` endpoint with a POST request.
   - Example:
     ```bash
     curl -X POST "http://127.0.0.1:8000/api/students/" \
       -H "Authorization: Bearer <access_token>" \
       -H "Content-Type: application/json" \
       -d '{"name": "John Doe", "email": "john@example.com"}'
     ```

4. **Get all students:**
   - Use the `/api/students/` endpoint with a GET request.
   - Example:
     ```bash
     curl -X GET "http://127.0.0.1:8000/api/students/" \
       -H "Authorization: Bearer <access_token>"
     ```

5. **Create a new course:**
   - Use the `/api/courses/` endpoint with a POST request.
   - Example:
     ```bash
     curl -X POST "http://127.0.0.1:8000/api/courses/" \
       -H "Authorization: Bearer <access_token>" \
       -H "Content-Type: application/json" \
       -d '{"title": "Math 101", "description": "Basic Mathematics"}'
     ```

6. **Get all courses:**
   - Use the `/api/courses/` endpoint with a GET request.
   - Example:
     ```bash
     curl -X GET "http://127.0.0.1:8000/api/courses/" \
       -H "Authorization: Bearer <access_token>"
     ```

7. **Access the interactive API docs:**
   - Open your browser and go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - You can try all endpoints directly from the Swagger UI.

**Note:** Replace `<access_token>` with the token received from the login step.

Docker & Docker Compose Guidelines
-------------------------------
1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   This will build the Docker image and start the FastAPI app at http://localhost:8000.

2. **Dockerfile**
   - Uses Python 3.13-slim as the base image.
   - Installs dependencies from requirements.txt.
   - Copies the project code and runs the app with Uvicorn.

3. **docker-compose.yml**
   - Builds the app container from the Dockerfile.
   - Exposes port 8000.
   - Mounts the project directory for live code reload (development).

4. **Official References:**
   - FastAPI Docker: https://fastapi.tiangolo.com/deployment/docker/
   - Docker Compose: https://docs.docker.com/compose/gettingstarted/
   - Python Docker: https://docs.docker.com/language/python/

5. **Stopping the containers:**
   ```bash
   docker-compose down
   ```

6. **Customizing for production:**
   - Remove the volume mount for code if you want a static image.
   - Add a production-ready database service (e.g., PostgreSQL) as needed.

Yes, you can find example Dockerfile and docker-compose.yml files for FastAPI and Python projects on official sites:

The official FastAPI documentation provides a Docker deployment guide.
The Docker documentation has Python-specific Dockerfile examples.
The docker-compose documentation provides general usage and examples.


https://fastapi.tiangolo.com/deployment/docker/

https://docs.docker.com/guides/python/

https://docs.docker.com/compose/gettingstarted/

Redis is used with FastAPI primarily to enhance performance and scalability through caching, session management, background task queuing, and real-time features like Pub/Sub. The modern redis-py library supports asynchronous operations, integrating seamlessly with FastAPI's async design.