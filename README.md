# FastAPI06-2 - User Authentication Backend

A FastAPI backend application with user authentication, featuring local login with JWT tokens and support for future GitHub OAuth integration.

## Features

- **User Registration** - Create new user accounts with username, email, full name, and password
- **User Login** - Authenticate with username and password, receive JWT access token
- **Protected Routes** - Access restricted endpoints with valid JWT token
- **Password Security** - Uses Argon2 for secure password hashing
- **JWT Authentication** - Token-based authentication with configurable expiration
- **PostgreSQL Database** - Robust relational database storage
- **CORS Enabled** - Configured for frontend development (localhost:5173)

## Project Structure

```
FastAPI06-2/
├── main.py              # FastAPI application entry point
├── database.py          # Database connection and session management
├── utils.py             # Authentication utilities (JWT, password hashing)
├── models/
│   └── user.py          # User model and Pydantic schemas
├── routers/
│   └── users.py         # User API routes
├── .env.example         # Environment variables template
├── .env                 # Environment variables (not committed)
└── README.md            # This file
```

## Requirements

- Python 3.8+
- PostgreSQL database
- Dependencies from `requirements.txt` (if created)

## Installation

1. **Clone the repository and navigate to the project directory:**

   ```bash
   cd FastAPI06-2
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv argon2-cffi python-jose pydantic
   ```

4. **Configure environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your database and JWT settings
   ```

5. **Update `.env` with your configuration:**

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=your_user
   DB_PASSWORD=your_password

   JWT_SECRET_KEY=your_secret_key_here
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## Running the Application

1. **Start the FastAPI server:**

   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

| Method | Endpoint          | Description             | Auth Required |
| ------ | ----------------- | ----------------------- | ------------- |
| POST   | `/users/register` | Register a new user     | No            |
| POST   | `/users/login`    | Login and get JWT token | No            |
| GET    | `/users/all`      | Get all users           | Yes           |

### Root

| Method | Endpoint | Description                    |
| ------ | -------- | ------------------------------ |
| GET    | `/`      | Welcome message and route list |

## Request/Response Examples

### Register User

**Request:**

```json
POST /users/register
{
  "username": "johndoe",
  "fullname": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**

```json
{
  "username": "johndoe",
  "email": "john@example.com"
}
```

### Login

**Request:**

```json
POST /users/login
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:**

```json
{
  "message": "Login successful",
  "username": "johndoe",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access_token_type": "bearer"
}
```

### Get All Users (Protected)

**Request:**

```http
GET /users/all
Authorization: Bearer <your_access_token>
```

**Response:**

```json
[
  {
    "username": "johndoe",
    "email": "john@example.com"
  },
  {
    "username": "janedoe",
    "email": "jane@example.com"
  }
]
```

## Environment Variables

| Variable                      | Description                | Default     |
| ----------------------------- | -------------------------- | ----------- |
| `DB_HOST`                     | PostgreSQL host            | `localhost` |
| `DB_PORT`                     | PostgreSQL port            | `5432`      |
| `DB_USER`                     | PostgreSQL username        | -           |
| `DB_PASSWORD`                 | PostgreSQL password        | -           |
| `JWT_SECRET_KEY`              | Secret key for JWT signing | -           |
| `JWT_ALGORITHM`               | JWT algorithm              | `HS256`     |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time      | `30`        |

## Database Schema

The `users` table includes the following columns:

| Column            | Type    | Description                                   |
| ----------------- | ------- | --------------------------------------------- |
| `id`              | Integer | Primary key                                   |
| `username`        | String  | Unique username                               |
| `fullname`        | String  | User's full name                              |
| `email`           | String  | Unique email address                          |
| `hashed_password` | String  | Argon2 hashed password                        |
| `github_id`       | String  | GitHub OAuth ID (future)                      |
| `avatar_url`      | String  | Profile avatar URL (future)                   |
| `auth_provider`   | String  | Authentication provider (`local` or `github`) |
