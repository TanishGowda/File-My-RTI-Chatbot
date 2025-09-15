# FileMyRTI AI Chatbot - Backend Setup Guide

This guide will help you set up the complete backend infrastructure for the FileMyRTI AI Chatbot project.

## 🏗️ Architecture Overview

The backend consists of:
1. **Supabase** - Authentication, database, and vector storage
2. **Python FastAPI** - AI service with OpenAI integration
3. **React Frontend** - User interface (already implemented)

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Supabase account
- OpenAI API key

## 🚀 Setup Instructions

### 1. Supabase Setup

1. **Create a Supabase project:**
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Note down your project URL and anon key

2. **Set up the database:**
   - Go to the SQL Editor in your Supabase dashboard
   - Run the SQL script from `supabase/schema.sql`
   - This will create all necessary tables and functions

3. **Enable Google OAuth (optional):**
   - Go to Authentication > Providers in Supabase dashboard
   - Enable Google provider
   - Add your Google OAuth credentials

### 2. Python Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your actual values:
   ```env
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_ANON_KEY=your_supabase_anon_key_here
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small
   DATABASE_URL=postgresql://postgres:password@localhost:5432/rti_chatbot
   SECRET_KEY=your_secret_key_here
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
   ```

5. **Start the backend server:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### 3. React Frontend Setup

1. **Navigate to project root:**
   ```bash
   cd ..  # if you're in backend directory
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your actual values:
   ```env
   REACT_APP_SUPABASE_URL=your_supabase_url_here
   REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key_here
   REACT_APP_API_URL=http://localhost:8000/api/v1
   ```

4. **Start the frontend:**
   ```bash
   npm start
   ```

## 🔧 Configuration Details

### Supabase Configuration

- **URL**: Your Supabase project URL
- **Anon Key**: Public key for client-side operations
- **Service Role Key**: Private key for server-side operations (keep secret!)

### OpenAI Configuration

- **API Key**: Get from [OpenAI Platform](https://platform.openai.com)
- **Model**: `gpt-4o-mini` (cost-effective) or `gpt-4` (more capable)
- **Embedding Model**: `text-embedding-3-small` for vector embeddings

### Database Schema

The database includes these main tables:
- `profiles` - User profiles
- `conversations` - Chat conversations
- `messages` - Individual messages
- `rti_drafts` - Generated RTI drafts
- `rti_filings` - Paid filing records
- `knowledge_base` - RAG knowledge base with vector embeddings

## 🧪 Testing the Setup

1. **Start both servers:**
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

2. **Test authentication:**
   - Go to `http://localhost:3000`
   - Try signing up with email/password
   - Try Google OAuth (if configured)

3. **Test AI chat:**
   - Create a new conversation
   - Ask RTI-related questions
   - Verify AI responses are generated

4. **Test API endpoints:**
   - Visit `http://localhost:8000/docs` for API documentation
   - Test endpoints using the interactive Swagger UI

## 🔍 Troubleshooting

### Common Issues

1. **CORS errors:**
   - Ensure `ALLOWED_ORIGINS` includes your frontend URL
   - Check that both servers are running

2. **Authentication errors:**
   - Verify Supabase credentials are correct
   - Check that RLS policies are properly set up

3. **AI response errors:**
   - Verify OpenAI API key is valid
   - Check that you have sufficient API credits

4. **Database connection errors:**
   - Ensure Supabase project is active
   - Verify database URL is correct

### Logs and Debugging

- **Backend logs:** Check terminal where you started the Python server
- **Frontend logs:** Check browser console
- **Supabase logs:** Check Supabase dashboard > Logs

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🚀 Deployment

### Backend Deployment (Python)

1. **Using Railway:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Deploy
   railway login
   railway init
   railway up
   ```

2. **Using Heroku:**
   ```bash
   # Install Heroku CLI
   # Create Procfile with: web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   heroku create your-app-name
   git push heroku main
   ```

### Frontend Deployment (React)

1. **Build for production:**
   ```bash
   npm run build
   ```

2. **Deploy to Vercel/Netlify:**
   - Connect your GitHub repository
   - Set environment variables
   - Deploy automatically

### Supabase Deployment

- Supabase handles hosting automatically
- No additional deployment steps needed

## 🔐 Security Considerations

1. **Environment Variables:**
   - Never commit `.env` files
   - Use different keys for development/production

2. **API Keys:**
   - Rotate keys regularly
   - Use least-privilege access

3. **Database Security:**
   - RLS policies are enabled
   - Service role key should be server-side only

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the API documentation
3. Check Supabase and OpenAI documentation
4. Create an issue in the project repository

## 🎯 Next Steps

After setup:
1. Add more knowledge base content for better RAG
2. Implement payment processing for RTI filing
3. Add more RTI-specific features
4. Optimize AI responses for RTI use cases
5. Add analytics and monitoring
