# 1. Django Migrations

Migrations track and apply database schema changes based on changes to Django models.

**Step 1: Update the model**

In `tasks/models.py`, add the following field to the `Task` model:

```python
date = models.DateTimeField(auto_now_add=True)
```

- `DateTimeField` stores a date and time.
- `auto_now_add=True` sets the field when the object is first created.

**Step 2: Generate migration files**

```bash
python manage.py makemigrations
```

Creates migration files describing detected model changes.

**Step 3: Apply migrations**

```bash
python manage.py migrate
```

Applies unapplied migrations to the database.

**Remember:**
- `makemigrations` -> generates migration files.
- `migrate` -> applies migrations to the database.

Changing `models.py` alone does not update the database schema.

# 2. How a POST Request Works

A POST request commonly creates a resource through an API.

1. The client prepares the task data as JSON.
2. The client sends a POST request to `/api/tasks/`.
3. The server validates the data and checks permissions.
4. If valid, the server saves the task to the database.
5. The server returns an HTTP response, commonly `201 Created` with the new task's data.

**Restaurant analogy:**

- Request: `CUSTOMER -> WAITER -> KITCHEN`
- Response: `CUSTOMER <- WAITER <- KITCHEN`

The client sends a request, and the server processes it and returns a response.

**API versus server:**

- **API:** Defines how applications communicate, including endpoints and request formats.
- **Server:** Receives and processes requests.

A server can expose an API.

# 3. HTTP Status Codes

| Status code | Meaning | Example |
|---|---|---|
| `200 OK` | Request succeeded. | GET or successful PATCH |
| `201 Created` | A resource was created. | Successful POST |
| `400 Bad Request` | Submitted data is invalid. | Serializer validation fails |
| `404 Not Found` | Resource does not exist. | Requested task ID is missing |

# 4. Django URL Configuration

Django projects commonly use two URL configuration files.

**`config/urls.py`**

The main URL configuration. It defines project-level routes and can delegate routing to individual apps using `include()`.

```python
path("admin/", admin.site.urls)
path("api/tasks/", include("tasks.urls"))
```

**`tasks/urls.py`**

Contains routes for task-related operations, such as listing, creating, retrieving, updating, and deleting tasks.

**Remember:**
- `config/urls.py` -> central project routing.
- `tasks/urls.py` -> task-specific routing.
- `include()` connects the app's URL configuration to the main URL configuration.

# 5. URL Parameters and Path Converters

A path converter captures part of a URL and passes it to the view.

```python
path("api/tasks/<int:pk>/", ...)
```

- `int` -> accepts an integer.
- `pk` -> parameter name, commonly meaning primary key.

For a request to `GET /api/tasks/1/`, Django captures `1` and passes it to the matched view as `pk=1`.

The view uses this value to look up the task. If the task does not exist, the API can return `404 Not Found`.

**Important:** The parameter name in the URL pattern must match the parameter expected by the view. For example, `<int:pk>` passes `pk`, while `<int:task_id>` passes `task_id`.