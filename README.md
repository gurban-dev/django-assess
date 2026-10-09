# Django Task API: Lesson and Coding Assessment

This small project provides a working Django REST Framework (DRF) list/create API for a teaching demonstration, followed by an intentionally unfinished coding assessment. It uses SQLite and Django's built-in authentication system.

## 1. Setup and Run

From the project directory, follow these steps to set up and run the application.

### Step 1: Create and Activate a Virtual Environment (Optional)

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it using the appropriate command for your operating system.

**Linux:**

```bash
source .venv/bin/activate
```

**Windows (Command Prompt):**

```bat
.venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Apply Database Migrations

```bash
python manage.py migrate
```

This applies the existing migrations and creates the necessary database tables.

The project already includes its initial migration file for the `Task` model. Migration files are committed to the repository so that anyone cloning the project can recreate the intended database schema without generating the initial migrations themselves.

Therefore, you do not need to run `python manage.py makemigrations` during the initial setup.

### Step 4: Start the Development Server

```bash
python manage.py runserver
```

The development server will be available at `http://127.0.0.1:8000/`.

### Step 5: Run Tests

Open a new terminal while python manage.py runserver is running and run the following:

```bash
python manage.py test
```

This runs the automated tests for the project. The demonstration tests should pass, while assessment tests may fail until the student implements the required functionality.

## 2. Demonstration

The working demonstration consists of two endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/tasks/` | Retrieve all tasks |
| POST | `/api/tasks/` | Create a task |

To create a task, send a POST request with a JSON body such as:

```json
{
  "title": "Prepare lesson",
  "completed": false
}
```

You can use a REST client, such as the Django REST Framework browsable API, to interact with these endpoints.

### Project Structure

The main files used in the demonstration are:

- `tasks/models.py`: Defines the `Task` model.
- `tasks/serializers.py`: Defines the `TaskSerializer` using `ModelSerializer`.
- `tasks/views.py`: Implements the list/create API view using `APIView`.
- `tasks/urls.py`: Defines the task API routes.
- `config/urls.py`: Includes the task routes in the project URL configuration.
- `tasks/tests.py`: Contains automated tests.

### Routes

These routes are currently registered by the project:

| Method | URL | Purpose |
|---|---|---|
| GET | `/api/tasks/` | List all tasks; open this URL in a browser to view the DRF browsable API. |
| POST | `/api/tasks/` | Create a task by sending JSON to the API. |
| GET, POST | `/admin/` | Django's admin site (sign in with a superuser account). |

The individual-task routes `GET`, `PATCH`, and `DELETE /api/tasks/<id>/` are assessment requirements and have not been added yet.

### Concepts Covered

The demonstration provides examples of:

- Django models and database migrations.
- QuerySets and retrieving database records.
- Serializing model instances with `many=True`.
- Processing incoming request data.
- Serializer validation and saving.
- DRF responses and HTTP status codes.
- URL routing and API views.

You can create an administrator account if you want to inspect tasks through Django's admin interface at `http://127.0.0.1:8000/admin/`.

```bash
python manage.py createsuperuser
```

### Resetting the Database

For a fresh local development database, stop the server and delete `db.sqlite3`. Then run:

```bash
python manage.py migrate
```

This recreates the database using the migrations included in the project. Deleting the database permanently removes its stored data, including tasks and user accounts, so only do this when you are comfortable losing that data.

## 3. Working with Database Migrations

Django migrations track changes to the database schema as your models evolve.

The two main commands serve different purposes:

- `python manage.py makemigrations` generates migration files based on changes to your models.
- `python manage.py migrate` applies existing migration files to the database.

### When Should You Run `makemigrations`?

Run it when you create a model or modify an existing model and need Django to generate a migration for the change.

For example, if you add a `description` field to the `Task` model, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

The first command generates a migration file describing the change. The second applies that change to the database.

Migration files should generally be committed to version control so that other developers can apply the same schema changes in the correct order.

For this project, the initial migration is already provided. However, the coding assessment requires associating tasks with users, which involves changing the model. You will need to generate and apply a new migration as part of that work.

## 4. Coding Assessment

### Django/DRF Coding Assessment: Extend the Task API

You are given an existing Task API that supports listing and creating tasks. Extend it to support individual tasks and ownership.

**Requirements**

1. Implement retrieving an individual task at `GET /api/tasks/<id>/`.
2. Implement partial updates at `PATCH /api/tasks/<id>/`.
3. Implement deletion at `DELETE /api/tasks/<id>/`.
4. Associate every task with a user using Django's built-in user model.
5. When an authenticated user creates a task, automatically assign that user as its owner. Do not accept the owner from client input.
6. Require authentication where appropriate and prevent users from viewing or modifying tasks owned by someone else.
7. Reject task titles that are empty or contain only whitespace.
8. Return appropriate HTTP status codes, including a clear response when a task does not exist.

### Implementation Guidance

The working list/create example is your starting point. You will need to:

- Update the `Task` model to include ownership.
- Generate and apply the necessary database migration.
- Update the serializer to handle the new requirements.
- Implement the individual-task view and its HTTP methods.
- Add the individual-task URL.
- Use `request.user` to identify the authenticated user.
- Add or update tests to verify the expected behavior.

The assessment tests in `tasks/tests.py` describe the expected behavior and are intended to fail until you implement the relevant requirements.

**Important:** The individual-task functionality, ownership logic, and associated assessment solution are intentionally not implemented. You are expected to write and test that code yourself.

## 5. Final Verification

After completing the assessment, run the full test suite:

```bash
python manage.py test
```

Use the test results to identify missing functionality, correct errors, and verify that the implementation meets the requirements.
