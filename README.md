# The Insider

**Social Media for Hollywood**

A modern, full-stack social media platform designed specifically for the entertainment industry. Share behind-the-scenes moments, connect with industry professionals, and stay updated with the latest Hollywood buzz.

## 🎬 Features

- **Secure Authentication** - JWT-based user registration and login
- **Media Sharing** - Upload and share images and videos with captions
- **Real-time Feed** - Browse posts from the Hollywood community
- **Content Management** - Edit and delete your own posts
- **Responsive Design** - Optimized for desktop and mobile viewing
- **Cloud Storage** - Powered by ImageKit for fast, reliable media delivery

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - Modern Python SQL toolkit and ORM
- **PostgreSQL** - Production database (Neon)
- **SQLite** - Local development database
- **FastAPI Users** - Authentication and user management
- **ImageKit** - Media storage and transformation
- **Uvicorn** - ASGI server

### Frontend
- **Streamlit** - Interactive web application framework
- **Python** - Core programming language
- **Requests** - HTTP client for API communication

### Infrastructure
- **Render** - Cloud deployment platform
- **Neon** - Serverless PostgreSQL database
- **ImageKit** - CDN and media processing

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- UV package manager (recommended) or pip

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd the-insider
   ```

2. **Set up the backend**
   ```bash
   cd backend
   uv sync  # or pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the backend directory:
   ```env
   JWT_SECRET=your-jwt-secret-key
   IMAGEKIT_PRIVATE_KEY=your-imagekit-private-key
   # DATABASE_URL is optional for local development (uses SQLite by default)
   ```

4. **Start the backend server**
   ```bash
   uv run python main.py
   # Server will start on http://localhost:1999
   ```

5. **Set up the frontend**
   ```bash
   cd ../frontend
   pip install -r requirements.txt
   ```

6. **Start the frontend**
   ```bash
   streamlit run interface.py
   # App will open in your browser
   ```

## 📁 Project Structure

```
the-insider/
├── backend/
│   ├── src/
│   │   ├── app.py          # FastAPI application
│   │   ├── db.py           # Database models and configuration
│   │   ├── users.py        # User authentication
│   │   ├── images.py       # ImageKit configuration
│   │   └── schemas.py      # Pydantic models
│   ├── main.py             # Application entry point
│   └── pyproject.toml      # Dependencies and configuration
├── frontend/
│   ├── interface.py        # Streamlit application
│   └── requirements.txt    # Frontend dependencies
└── README.md
```

## 🌐 Deployment

### Backend (Render)
1. Connect your repository to Render
2. Create a new Web Service
3. Set environment variables:
   - `DATABASE_URL` - Your Neon PostgreSQL connection string
   - `JWT_SECRET` - Your JWT secret key
   - `IMAGEKIT_PRIVATE_KEY` - Your ImageKit private key
   - `APP_ENV=production`
4. Deploy with build command: `uv sync`
5. Start command: `uv run uvicorn src.app:app --host 0.0.0.0 --port $PORT`

### Frontend
Deploy the frontend using Streamlit Community Cloud or another Render Web Service.

## 🔧 Configuration

### Database
- **Local**: SQLite (`test.db`) - automatic fallback
- **Production**: PostgreSQL via Neon - set `DATABASE_URL` environment variable

### Authentication
- JWT-based authentication with FastAPI Users
- Secure password hashing with bcrypt
- Email-based user registration

### Media Storage
- ImageKit integration for image/video uploads
- Automatic image optimization and transformation
- CDN delivery for fast loading

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎭 About

The Insider is built for the entertainment industry, providing a dedicated platform for Hollywood professionals to share their work, connect with peers, and showcase behind-the-scenes content in a secure, professional environment.

---

**Built with ❤️ for Hollywood**
