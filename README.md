# E-commerce Dashboard

A modern full-stack e-commerce dashboard built with Next.js 16 and FastAPI, featuring real-time updates and comprehensive product management.

## 🚀 Features

- **User Authentication**: JWT-based login system
- **Product Management**: Full CRUD operations for products
- **Real-time Updates**: WebSocket integration for live data synchronization
- **Responsive Design**: Modern UI with Tailwind CSS
- **Type Safety**: Full TypeScript implementation
- **API Documentation**: Auto-generated OpenAPI docs

## 🏗️ Architecture

### Frontend (Next.js 16.1.6)
- React 19.2 with automatic memoization
- App Router for optimal performance
- Server Components for SEO
- Client-side state management
- Responsive design with Tailwind CSS

### Backend (FastAPI 0.133.0)
- Async API endpoints
- JWT authentication
- PostgreSQL integration
- WebSocket support
- Automatic API documentation

### Database
- PostgreSQL for reliable data storage
- Connection pooling
- Migration support

## 📁 Project Structure

```
.
├── e-commerce-backend/          # FastAPI backend
│   ├── main.py                 # Main application
│   ├── routers/                # API routes
│   ├── models/                 # Database models
│   └── config/                 # Configuration
├── e-commerce-frontend/         # Next.js frontend
│   ├── src/
│   │   ├── app/               # Next.js app router
│   │   ├── components/        # React components
│   │   ├── actions/           # Server actions
│   │   └── types/             # TypeScript types
│   └── public/                # Static assets
├── .github/workflows/          # CI/CD pipelines
└── DEPLOYMENT.md              # Deployment guide
```

## 🛠️ Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11, PostgreSQL
- **Testing**: Jest, pytest, Testing Library
- **Deployment**: Vercel (frontend), Railway (backend)
- **CI/CD**: GitHub Actions

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- PostgreSQL

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd e-commerce-dashboard
   ```

2. **Backend Setup**
   ```bash
   cd e-commerce-backend
   pip install -r requirements.txt
   # Set up your .env file
   uvicorn main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd e-commerce-frontend
   npm install
   npm run dev
   ```

4. **Database Setup**
   ```sql
   CREATE DATABASE ecommerce;
   -- Run migrations if applicable
   ```

## 📡 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Products
- `GET /api/products` - List products
- `POST /api/products` - Create product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### Real-time
- `WebSocket /ws/products` - Live updates

## 🧪 Testing

```bash
# Backend tests
cd e-commerce-backend
pytest

# Frontend tests
cd e-commerce-frontend
npm test
```

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 📞 Support

For questions or issues, please open an issue on GitHub.