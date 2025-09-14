## Agrigenie

Agrigenie is a Django-based platform that helps farmers and stakeholders with crop recommendations, weather insights, pesticide guidance, government schemes, soil testing reports, export information, and a voice/chat assistant.

### Key Features
- **Authentication**: User registration, login, profiles.
- **Crops**: Browse crops, view details, get recommendations and price forecasts.
- **Weather**: Weather dashboard with feels-like temperature and geo attributes.
- **Pesticides**: Database of pesticides with seed data loader.
- **Schemes**: Government schemes browsing and application helpers.
- **Soil**: Soil test input, history, PDF tools, and report generation.
- **Exports**: Export market info (list and detail views).
- **Voice Assistant**: Assistant, chatbot, and unified assistant UIs.

### Tech Stack
- **Backend**: Python 3.12+, Django, Django Rest Framework.
- **Database**: SQLite.
- **Frontend**: Html, CSS ,Javascript.

### Project Structure
```
agrigenie/
  manage.py
  agrigenie/           # Django project config (settings, urls, wsgi/asgi)
  apps/
    authentication/    # Auth app (forms, models, templates)
    crops/             # Crops data, recommendations, price forecasts
    exports/           # Export info
    pesticides/        # Pesticides data with populate command
    schemes/           # Government schemes with populate command
    soil/              # Soil test forms, history, report generation
    voice/             # Voice/chat assistant UIs
    weather/           # Weather dashboard and models
  templates/           # HTML templates (organized by app)
  static/              # Static assets (CSS/JS/images)
  requirements.txt
  db.sqlite3           # Local dev DB (auto-created)
```

### Getting Started
#### 1) Prerequisites
- Python 3.10+ recommended
- pip
- (Optional) Virtual environment tool (`venv`)

#### 2) Clone and set up environment
```bash
git clone <your-repo-url>
cd agrigenie
python -m venv .venv
# Windows PowerShell
. .venv\\Scripts\\Activate.ps1
# macOS/Linux
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3) Environment variables (optional)
By default, the project uses SQLite and sensible defaults from `agrigenie/settings.py`.
You can override via environment variables or a `.env` loader you add. Typical configs:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` ("1"/"0")
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `DATABASE_URL` (for Postgres/MySQL via `dj-database-url` if added)

#### 4) Apply migrations
```bash
python manage.py migrate
```

#### 5) Create a superuser (admin)
```bash
python manage.py createsuperuser
```

#### 6) Load sample/seed data (optional)
The repository includes management commands to quickly populate useful data:
- Pesticides:
```bash
python manage.py populate_pesticides
```
- Government schemes:
```bash
python manage.py populate_schemes
```
- Sample crops:
```bash
python manage.py load_sample_crops
```

You may also find `add_crops.py` for bulk add/import flows depending on your use case.

#### 7) Run the development server
```bash
python manage.py runserver
```
Open http://127.0.0.1:8000/ in your browser.

### Application Walkthrough
- **Authentication** (`apps/authentication`):
  - Templates: `templates/authentication/login.html`, `register.html`, `profile.html`
  - Configure context processors and template tags as needed (`context_processors.py`, `templatetags/`)

- **Crops** (`apps/crops`):
  - Recommendation form and results: `templates/crops/recommendation_form.html`, `recommendation_result.html`
  - List and detail: `templates/crops/crop_list.html`, `crop_detail.html`
  - Forecast models: see `apps/crops/models.py` (e.g., `CropPriceForecast`)
  - Utilities in `apps/crops/utils.py`

- **Weather** (`apps/weather`):
  - Dashboard: `templates/weather/dashboard.html`
  - Models include feels-like, latitude/longitude, etc. See `apps/weather/models.py`

- **Pesticides** (`apps/pesticides`):
  - Seed data loader: `apps/pesticides/management/commands/populate_pesticides.py`
  - Views and templates under `templates/pesticides/`

- **Schemes** (`apps/schemes`):
  - Seed data loader: `apps/schemes/management/commands/populate_schemes.py`
  - Application, list, detail views under `templates/schemes/`

- **Soil** (`apps/soil`):
  - Forms and reporting: `templates/soil/test_form.html`, `report.html`, `history.html`, `pdf_tools.html`

- **Exports** (`apps/exports`):
  - List and detail views: `templates/exports/list.html`, `detail.html`

- **Voice Assistant** (`apps/voice`):
  - Assistant UIs: `templates/voice/assistant.html`, `chatbot.html`, `unified_assistant.html`

Each app has its own `urls.py` and is included from the project router in `agrigenie/urls.py`.

### Common Commands
```bash
# Run server
python manage.py runserver

# Make migrations for model changes
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load sample data
python manage.py populate_pesticides
python manage.py populate_schemes
python manage.py load_sample_crops
```

### Static Files
In development, Django serves static files when `DEBUG=1`. For production, ensure `STATIC_ROOT` is configured and run:
```bash
python manage.py collectstatic --noinput
```

### Tests
```bash
python manage.py test
```

### Deployment Notes
- Set `DEBUG=0` and configure `ALLOWED_HOSTS`.
- Provide a secure `SECRET_KEY` via environment variable.
- Use a production database (Postgres/MySQL) and configure caches.
- Serve static/media via a web server or CDN.
- Run database migrations during deploy.

### Contributing
1. Create a feature branch.
2. Write clear, readable code and tests.
3. Open a PR describing changes.

### License
Add your preferred license here (e.g., MIT, Apache-2.0).

### Acknowledgements
Thanks to contributors and open-source libraries that made this project possible.


