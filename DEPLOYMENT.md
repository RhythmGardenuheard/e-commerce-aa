# E-commerce Dashboard - Deployment Guide

## Overview
This guide covers deploying the full-stack e-commerce dashboard application with Next.js frontend and FastAPI backend.

## Architecture
- **Frontend**: Next.js 16.1.6 with React 19.2, TypeScript, Tailwind CSS
- **Backend**: FastAPI 0.133.0 with PostgreSQL, JWT authentication
- **Database**: PostgreSQL
- **Real-time**: WebSocket for live updates

## Prerequisites
- Node.js 20+
- Python 3.11+
- PostgreSQL database
- GitHub account for CI/CD

## Local Development Setup

### Backend Setup
```bash
cd e-commerce-backend
pip install -r requirements.txt
# Set up environment variables in .env
DATABASE_URL=postgresql://user:password@localhost/ecommerce
SECRET_KEY=your-secret-key
# Run migrations (if using Alembic)
alembic upgrade head
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd e-commerce-frontend
npm install
npm run dev
```

## Production Deployment

### 1. Database Setup (PostgreSQL)
```sql
CREATE DATABASE ecommerce;
CREATE USER ecommerce_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO ecommerce_user;
```

### 2. Backend Deployment (Railway)
1. Create Railway account
2. Connect GitHub repository
3. Set environment variables:
   - `DATABASE_URL`
   - `SECRET_KEY`
4. Deploy automatically on push to main branch

### 3. Frontend Deployment (Vercel)
1. Create Vercel account
2. Connect GitHub repository
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL` (Railway backend URL)
4. Deploy automatically

### 4. Domain Configuration
- Point custom domain to Vercel
- Update CORS settings in FastAPI for production domain

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-256-bit-secret
CORS_ORIGINS=https://your-frontend-domain.com
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

## CI/CD Pipeline
The GitHub Actions workflow includes:
- Backend testing with pytest
- Frontend testing with Jest
- Automatic deployment on main branch push

## Monitoring & Maintenance
- Set up error tracking (Sentry)
- Configure logging
- Monitor performance metrics
- Regular security updates

## Scaling Considerations
- Use Redis for session caching
- Implement rate limiting
- Set up load balancing for backend
- Consider CDN for static assets

## Troubleshooting
- Check Railway/Vercel deployment logs
- Verify environment variables
- Test API endpoints with Postman
- Check database connectivity