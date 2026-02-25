# E-commerce Dashboard Backend

This is a FastAPI backend for an e-commerce dashboard with JWT authentication, product CRUD operations, and WebSocket real-time updates using Prisma for PostgreSQL.

## Features

- JWT User Authentication
- Product CRUD Operations
- WebSocket Real-time Updates
- Async Support
- Auto-generated Documentation

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL database and update DATABASE_URL in .env

3. Generate Prisma client:
   ```
   prisma generate
   ```

4. Run database migrations:
   ```
   prisma db push
   ```

5. Run the server:
   ```
   uvicorn main:app --reload
   ```

## API Documentation

Visit http://localhost:8000/docs for auto-generated API documentation.