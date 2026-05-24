# OctoFit Tracker — Backend Requirements

## Project Context

OctoFit Tracker is a fitness tracking web application built for Mergington High School. It allows students to log workouts, track activities, join teams, and compete on a leaderboard. The application was designed by a PE teacher (Paul Octo) with the school's IT department.

---

## Architecture Overview

- **Pattern:** REST API backend, decoupled from a separate frontend.
- **Backend server port:** `8000`
- **Database port:** `27017` (MongoDB, private)
- **Database name:** `octofit_db`
- **API base path:** `/api/`
- **Admin panel path:** `/admin/`
- **Root path (`/`):** Returns a JSON response with the resolved API root URL.

The backend is entirely responsible for data persistence, business logic, password validation, and serving the REST API. The frontend communicates with the backend exclusively via HTTP requests to the API endpoints.

---

## Technology Stack (as implemented)

| Component        | Technology                |
|------------------|--------------------------|
| Language         | Python 3                 |
| Web framework    | Django 4.1.7             |
| REST framework   | djangorestframework 3.14.0 |
| Database engine  | djongo 1.3.6 (MongoDB adapter) |
| MongoDB driver   | pymongo 3.12             |
| CORS handling    | django-cors-headers 4.5.0 |
| Auth helpers     | django-allauth 0.51.0, dj-rest-auth 2.2.6 |
| SQL parser       | sqlparse 0.2.4           |

---

## Directory Structure

```
octofit-tracker/
└── backend/
    ├── venv/
    ├── requirements.txt
    ├── manage.py
    └── octofit_tracker/
        ├── __init__.py
        ├── asgi.py
        ├── wsgi.py
        ├── settings.py
        ├── urls.py
        ├── models.py
        └── management/
            └── commands/
                └── populate_db.py
```

---

## Dependencies (requirements.txt)

```
Django==4.1.7
djangorestframework==3.14.0
django-allauth==0.51.0
django-cors-headers==4.5.0
dj-rest-auth==2.2.6
djongo==1.3.6
pymongo==3.12
sqlparse==0.2.4
stack-data==0.6.3
sympy==1.12
tenacity==9.0.0
terminado==0.18.1
threadpoolctl==3.5.0
tinycss2==1.3.0
tornado==6.4.1
traitlets==5.14.3
types-python-dateutil==2.9.0.20240906
typing_extensions==4.9.0
tzdata==2024.2
uri-template==1.3.0
urllib3==2.2.3
wcwidth==0.2.13
webcolors==24.8.0
webencodings==0.5.1
websocket-client==1.8.0
```

---

## Database Configuration

- **Engine:** `djongo` (MongoDB via Django ORM)
- **Database name:** `octofit_db`
- **Host:** `localhost`
- **Port:** `27017`
- **Authentication:** None (no username or password configured)
- **Schema enforcement:** `ENFORCE_SCHEMA = False`
- **Default primary key field type:** `BigAutoField`

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'octofit_db',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'localhost',
            'port': 27017,
        },
    }
}
```

---

## Authentication

- Uses Django's built-in `django.contrib.auth` user model (`User`).
- No custom user model — the standard `User` model is used directly.
- Users are created with `User.objects.create_user(username, email, password, first_name, last_name)`.
- Default password for seeded test users: `octofit2024`
- No JWT or token-based authentication is configured; standard session-based Django auth is available.
- `django-allauth` and `dj-rest-auth` are installed as dependencies but not explicitly configured beyond installation.

### Password Validation Rules (from settings.py)

The following validators are applied to all user passwords:

1. `UserAttributeSimilarityValidator` — password must not be too similar to user attributes
2. `MinimumLengthValidator` — password must meet a minimum length
3. `CommonPasswordValidator` — password must not be a commonly used password
4. `NumericPasswordValidator` — password must not be entirely numeric

---

## Data Models

All models are defined in `octofit_tracker/models.py`.

### User

Django's built-in `User` model. Fields used:

| Field        | Type        | Notes                        |
|--------------|-------------|------------------------------|
| `username`   | CharField   | Unique                       |
| `email`      | EmailField  |                              |
| `password`   | CharField   | Hashed by Django             |
| `first_name` | CharField   |                              |
| `last_name`  | CharField   |                              |
| `is_superuser` | BooleanField | Used to distinguish admin users |

---

### Team

```python
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
```

| Field         | Type      | Constraints         |
|---------------|-----------|---------------------|
| `name`        | CharField | max_length=100, unique |
| `description` | TextField | blank=True          |

---

### Workout

```python
class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
```

| Field         | Type      | Constraints  |
|---------------|-----------|--------------|
| `name`        | CharField | max_length=100 |
| `description` | TextField | blank=True   |

---

### Activity

```python
class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('run', 'Run'),
        ('walk', 'Walk'),
        ('strength', 'Strength'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    date = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)
```

| Field      | Type             | Constraints / Notes              |
|------------|------------------|----------------------------------|
| `user`     | ForeignKey(User) | CASCADE delete                   |
| `team`     | ForeignKey(Team) | CASCADE delete                   |
| `type`     | CharField        | Choices: `run`, `walk`, `strength` |
| `duration` | PositiveIntegerField | Duration in minutes           |
| `date`     | DateTimeField    | Auto-set on creation             |
| `points`   | IntegerField     | Default: 0                       |

---

### Leaderboard

```python
class Leaderboard(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    month = models.CharField(max_length=20)
```

| Field          | Type             | Constraints / Notes |
|----------------|------------------|---------------------|
| `team`         | ForeignKey(Team) | CASCADE delete      |
| `total_points` | IntegerField     | Default: 0          |
| `month`        | CharField        | max_length=20, e.g. `"2024-05"` |

---

## API Endpoints

The following endpoints are referenced by the frontend and defined/placeholdered in `urls.py`:

| Endpoint              | Method | Description                        |
|-----------------------|--------|------------------------------------|
| `/`                   | GET    | Returns JSON with resolved `api_root` URL |
| `/admin/`             | —      | Django admin panel                 |
| `/api/activities/`    | GET    | List all activities                |
| `/api/leaderboard/`   | GET    | List leaderboard entries           |
| `/api/teams/`         | GET    | List all teams                     |
| `/api/users/`         | GET    | List all users                     |
| `/api/workouts/`      | GET    | List all workouts                  |

### API Root Response

The root endpoint (`/`) returns the resolved API URL. If the `CODESPACE_NAME` environment variable is set (GitHub Codespaces), the URL uses the Codespace public domain:

```json
{ "api_root": "https://<CODESPACE_NAME>-8000.app.github.dev/api/" }
```

Otherwise:

```json
{ "api_root": "http://localhost:8000/api/" }
```

---

## CORS Configuration

```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']
CORS_ALLOW_METHODS = ['*']
```

All origins, headers, and methods are allowed.

---

## Allowed Hosts

```python
ALLOWED_HOSTS = ['*']
```

If `CODESPACE_NAME` environment variable is set, the Codespace URL is also explicitly appended:

```python
ALLOWED_HOSTS.append(f"{os.environ.get('CODESPACE_NAME')}-8000.app.github.dev")
```

---

## Installed Django Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'octofit_tracker',
    'rest_framework',
    'djongo',
    'corsheaders',
]
```

---

## Middleware (in order)

1. `SecurityMiddleware`
2. `SessionMiddleware`
3. `CorsMiddleware`
4. `CommonMiddleware`
5. `CsrfViewMiddleware`
6. `AuthenticationMiddleware`
7. `MessageMiddleware`
8. `XFrameOptionsMiddleware`

---

## Internationalization

| Setting         | Value    |
|-----------------|----------|
| `LANGUAGE_CODE` | `en-us`  |
| `TIME_ZONE`     | `UTC`    |
| `USE_I18N`      | `True`   |
| `USE_TZ`        | `True`   |

---

## Seed / Test Data (`populate_db` management command)

The `populate_db` command (`python manage.py populate_db`) clears and repopulates the database with:

### Teams

| Name         | Description                         |
|--------------|-------------------------------------|
| Team Marvel  | Marvel superheroes fitness team     |
| Team DC      | DC superheroes fitness team         |

### Users

| Username    | Email                   | First Name | Last Name | Team        |
|-------------|-------------------------|------------|-----------|-------------|
| ironman     | ironman@marvel.com      | Tony       | Stark     | Team Marvel |
| spiderman   | spiderman@marvel.com    | Peter      | Parker    | Team Marvel |
| thor        | thor@marvel.com         | Thor       | Odinson   | Team Marvel |
| batman      | batman@dc.com           | Bruce      | Wayne     | Team DC     |
| superman    | superman@dc.com         | Clark      | Kent      | Team DC     |
| wonderwoman | wonderwoman@dc.com      | Diana      | Prince    | Team DC     |

All users are created with password: `octofit2024`

### Activities (per user)

| Type     | Duration | Points |
|----------|----------|--------|
| run      | 30 min   | 30     |
| strength | 45 min   | 45     |

### Workouts

| Name               | Description                              |
|--------------------|------------------------------------------|
| Morning Run        | 5km morning run for cardio               |
| Strength Training  | Full body strength workout               |
| Yoga Flow          | Relaxing yoga session for flexibility    |

### Leaderboard

- One entry per team, with `total_points` summed from all team activities.
- Month: `"2024-05"`

---

## Functional Requirements

1. The backend must expose a REST API consumed by the frontend over HTTP.
2. The API must serve lists of users, teams, activities, workouts, and leaderboard entries.
3. Activities must be linked to both a user and a team.
4. Each activity must record its type (run, walk, or strength), duration in minutes, date/time, and points.
5. The leaderboard must aggregate total points per team, per month.
6. The backend must support Django's admin panel at `/admin/`.
7. The root endpoint must return the correct resolved API URL, accounting for GitHub Codespaces environments.
8. A management command must exist to seed the database with test data.
9. All existing data must be cleared before seeding.
10. Password validation must enforce similarity, minimum length, common password, and numeric-only checks.

---

## Non-Functional Requirements

1. `DEBUG = True` in the current configuration (development only).
2. The backend runs on port `8000`.
3. MongoDB runs on port `27017` (private, not exposed externally).
4. No database authentication is configured; MongoDB is accessed without credentials.
5. CORS is fully open (all origins, headers, methods).
6. The `CODESPACE_NAME` environment variable is used to dynamically construct public-facing API URLs for GitHub Codespaces deployments.
7. Timezone is UTC; timezone-aware datetimes are used (`USE_TZ = True`).
8. All static files are served from the `static/` URL path.
