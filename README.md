# fasty-blog-py

A full-stack blogging platform built with **FastAPI**, **SQLite**, and **Tailwind CSS**. Users can register, log in, create and manage posts, and browse content from other users — all through a server-rendered UI backed by a REST API.

---

## Features

- User registration and authentication (JWT / OAuth2)
- Create, edit, and delete blog posts
- User profile pages with profile pictures
- Home feed listing all posts
- Fully async backend with SQLAlchemy + aiosqlite
- Server-side rendering via Jinja2 templates
- REST API with JSON responses alongside the HTML views
- Docker-ready deployment (Gunicorn + Uvicorn workers)

---

## Tech Stack

| Layer      | Technology                                        |
| ---------- | ------------------------------------------------- |
| Framework  | FastAPI                                           |
| Database   | SQLite (async via `aiosqlite` + SQLAlchemy 2.0)   |
| Auth       | JWT (`pyjwt`), Argon2 password hashing (`pwdlib`) |
| Templates  | Jinja2                                            |
| Styling    | Tailwind CSS                                      |
| Server     | Gunicorn + Uvicorn workers                        |
| Deployment | Docker                                            |

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+ _(only needed to recompile Tailwind CSS)_

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd fasty-blog-py

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run (development)

```bash
fastapi dev main.py
```

The app will be available at `http://localhost:8000`. The SQLite database (`blog.db`) is created automatically on first startup.

---

## Docker

```bash
# Build the image (Tailwind CSS is compiled in a multi-stage build)
docker build -t fasty-blog .

# Run the container
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e PORT=8000 \
  fasty-blog
```

The container uses Gunicorn with 3 Uvicorn workers and listens on `$PORT` (defaults to `8000`). Suitable for deployment on platforms like Render.

---

## API Reference

### Authentication

| Method | Endpoint           | Description                        |
| ------ | ------------------ | ---------------------------------- |
| `POST` | `/api/users/token` | Login — returns a JWT access token |

Tokens use the **Bearer** scheme: `Authorization: Bearer <token>`

### Users

| Method   | Endpoint                     | Auth     | Description                |
| -------- | ---------------------------- | -------- | -------------------------- |
| `POST`   | `/api/users`                 | —        | Register a new user        |
| `GET`    | `/api/users/me`              | ✓        | Current authenticated user |
| `GET`    | `/api/users/{user_id}`       | —        | User profile               |
| `GET`    | `/api/users/{user_id}/posts` | —        | Posts by a user            |
| `PATCH`  | `/api/users/{user_id}`       | ✓ (self) | Update profile             |
| `DELETE` | `/api/users/{user_id}`       | ✓ (self) | Delete account             |

### Posts

| Method   | Endpoint               | Auth      | Description       |
| -------- | ---------------------- | --------- | ----------------- |
| `GET`    | `/api/posts`           | —         | List all posts    |
| `GET`    | `/api/posts/{post_id}` | —         | Get a single post |
| `POST`   | `/api/posts`           | ✓         | Create a post     |
| `PUT`    | `/api/posts/{post_id}` | ✓ (owner) | Full update       |
| `PATCH`  | `/api/posts/{post_id}` | ✓ (owner) | Partial update    |
| `DELETE` | `/api/posts/{post_id}` | ✓ (owner) | Delete a post     |

---

## Project Structure

```
fasty-blog-py/
├── main.py           # App entry point, static/media mounts
├── auth.py           # JWT creation and verification
├── config.py         # Settings from environment variables
├── database.py       # Async SQLAlchemy engine and session
├── models.py         # ORM models (User, Post)
├── schemas.py        # Pydantic schemas for validation
├── routers/
│   ├── posts.py      # Post API + HTML routes
│   └── users.py      # User API + auth routes
├── templates/        # Jinja2 HTML templates
├── static/           # CSS, JS, icons
├── media/            # Uploaded profile pictures
└── Dockerfile        # Multi-stage build (Node → Python)
```
