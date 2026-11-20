# django-blog-cms

> Markdown blog CMS with tags, comments and SEO.

[![CI](https://github.com/dblzroch/django-blog-cms/actions/workflows/ci.yml/badge.svg)](https://github.com/dblzroch/django-blog-cms/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](pyproject.toml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Django 5.0+](https://img.shields.io/badge/django-5.0+-blue.svg)](https://www.djangoproject.com/)

Blog CMS built with [Django](https://www.djangoproject.com/).
Write posts in Markdown, organize with tags, moderate comments and get automatic sitemap/SEO.

## Quickstart

```bash
# Clone
git clone https://github.com/dblzroch/django-blog-cms.git
cd django-blog-cms

# Install (uv)
uv sync --dev

# Migrate
uv run python manage.py migrate

# Create superuser (admin access)
uv run python manage.py createsuperuser

# Run the development server
uv run python manage.py runserver
```

## How it works

- **Framework**: Django 5.x with built-in admin, ORM and authentication.
- **Storage**: SQLite (dev) / PostgreSQL (production-ready via DATABASE_URL).
- **Features**: Write posts in Markdown, tag system, comment moderation (pending/approved),
  sitemap.xml and SEO meta tags, Django admin for content management.
- **Tests**: `pytest` + `pytest-django` with coverage gate at 80%.
- **CI**: GitHub Actions runs ruff, mypy and pytest on every push/PR.

## Tests & quality

```bash
make test      # pytest with coverage
make lint      # ruff + mypy
make fmt       # ruff format
make migrate   # apply database migrations
```

## License

MIT
