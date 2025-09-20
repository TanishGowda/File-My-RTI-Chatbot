-- FileMyRTI AI Chatbot Database Schema
-- This file contains all the SQL commands to set up the database schema

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Note: pgvector extension needs to be enabled in Supabase dashboard first
-- Go to Database > Extensions and enable pgvector
-- CREATE EXTENSION IF NOT EXISTS "pgvector";

-- Create profiles table
CREATE TABLE profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  full_name TEXT,
  email TEXT UNIQUE,
  phone_number TEXT,
  address TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create conversations table
CREATE TABLE conversations (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create messages table
CREATE TABLE messages (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  sender TEXT NOT NULL CHECK (sender IN ('user', 'bot')),
  content TEXT NOT NULL,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create RTI drafts table
CREATE TABLE rti_drafts (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  department TEXT,
  subject TEXT,
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'submitted', 'filed', 'rejected')),
  application_number TEXT,
  filing_fee DECIMAL(10,2) DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create RTI filings table (for paid filing service)
CREATE TABLE rti_filings (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  rti_draft_id UUID REFERENCES rti_drafts(id) ON DELETE CASCADE,
  payment_id TEXT,
  payment_status TEXT DEFAULT 'pending' CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
  filing_status TEXT DEFAULT 'pending' CHECK (filing_status IN ('pending', 'submitted', 'acknowledged', 'rejected')),
  application_number TEXT,
  pio_email TEXT,
  pio_address TEXT,
  submission_date TIMESTAMP WITH TIME ZONE,
  acknowledgment_date TIMESTAMP WITH TIME ZONE,
  response_date TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create PDF documents table for RAG
CREATE TABLE pdf_documents (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  file_name TEXT NOT NULL,
  file_data TEXT NOT NULL, -- Store as base64 encoded string
  file_size INTEGER NOT NULL,
  file_type TEXT DEFAULT 'application/pdf',
  extracted_text TEXT NOT NULL,
  embedding VECTOR(1536), -- Vector embedding for semantic search
  rti_category TEXT, -- Category like 'land_records', 'employment', 'education', etc.
  rti_department TEXT, -- Specific department this format applies to
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX idx_rti_drafts_user_id ON rti_drafts(user_id);
CREATE INDEX idx_rti_drafts_status ON rti_drafts(status);
CREATE INDEX idx_rti_filings_user_id ON rti_filings(user_id);
CREATE INDEX idx_rti_filings_payment_status ON rti_filings(payment_status);
CREATE INDEX idx_pdf_documents_rti_category ON pdf_documents(rti_category);
CREATE INDEX idx_pdf_documents_rti_department ON pdf_documents(rti_department);
-- Vector index for semantic search
CREATE INDEX idx_pdf_documents_embedding ON pdf_documents USING ivfflat (embedding vector_cosine_ops);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_rti_drafts_updated_at BEFORE UPDATE ON rti_drafts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_rti_filings_updated_at BEFORE UPDATE ON rti_filings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_pdf_documents_updated_at BEFORE UPDATE ON pdf_documents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE rti_drafts ENABLE ROW LEVEL SECURITY;
ALTER TABLE rti_filings ENABLE ROW LEVEL SECURITY;
ALTER TABLE pdf_documents ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON profiles FOR INSERT WITH CHECK (auth.uid() = id);

-- Conversations policies
CREATE POLICY "Users can view own conversations" ON conversations FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own conversations" ON conversations FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own conversations" ON conversations FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own conversations" ON conversations FOR DELETE USING (auth.uid() = user_id);

-- Messages policies
CREATE POLICY "Users can view messages from own conversations" ON messages FOR SELECT 
  USING (conversation_id IN (SELECT id FROM conversations WHERE user_id = auth.uid()));
CREATE POLICY "Users can insert messages to own conversations" ON messages FOR INSERT 
  WITH CHECK (conversation_id IN (SELECT id FROM conversations WHERE user_id = auth.uid()));
CREATE POLICY "Users can update messages from own conversations" ON messages FOR UPDATE 
  USING (conversation_id IN (SELECT id FROM conversations WHERE user_id = auth.uid()));
CREATE POLICY "Users can delete messages from own conversations" ON messages FOR DELETE 
  USING (conversation_id IN (SELECT id FROM conversations WHERE user_id = auth.uid()));

-- RTI drafts policies
CREATE POLICY "Users can view own RTI drafts" ON rti_drafts FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own RTI drafts" ON rti_drafts FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own RTI drafts" ON rti_drafts FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own RTI drafts" ON rti_drafts FOR DELETE USING (auth.uid() = user_id);

-- RTI filings policies
CREATE POLICY "Users can view own RTI filings" ON rti_filings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own RTI filings" ON rti_filings FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own RTI filings" ON rti_filings FOR UPDATE USING (auth.uid() = user_id);

-- PDF documents are public read-only for RAG
CREATE POLICY "PDF documents are publicly readable" ON pdf_documents FOR SELECT USING (true);

-- Create functions for common operations
CREATE OR REPLACE FUNCTION get_user_conversations(user_uuid UUID)
RETURNS TABLE (
  id UUID,
  title TEXT,
  created_at TIMESTAMP WITH TIME ZONE,
  updated_at TIMESTAMP WITH TIME ZONE,
  message_count BIGINT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    c.id,
    c.title,
    c.created_at,
    c.updated_at,
    COUNT(m.id) as message_count
  FROM conversations c
  LEFT JOIN messages m ON c.id = m.conversation_id
  WHERE c.user_id = user_uuid
  GROUP BY c.id, c.title, c.created_at, c.updated_at
  ORDER BY c.updated_at DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get conversation messages
CREATE OR REPLACE FUNCTION get_conversation_messages(conv_id UUID, user_uuid UUID)
RETURNS TABLE (
  id UUID,
  sender TEXT,
  content TEXT,
  created_at TIMESTAMP WITH TIME ZONE,
  metadata JSONB
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    m.id,
    m.sender,
    m.content,
    m.created_at,
    m.metadata
  FROM messages m
  JOIN conversations c ON m.conversation_id = c.id
  WHERE c.id = conv_id AND c.user_id = user_uuid
  ORDER BY m.created_at ASC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to search PDF documents using vector similarity
CREATE OR REPLACE FUNCTION search_pdf_documents(query_embedding VECTOR(1536), match_threshold FLOAT DEFAULT 0.5, match_count INT DEFAULT 5)
RETURNS TABLE (
  id UUID,
  title TEXT,
  description TEXT,
  file_name TEXT,
  extracted_text TEXT,
  rti_category TEXT,
  rti_department TEXT,
  similarity FLOAT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    pd.id,
    pd.title,
    pd.description,
    pd.file_name,
    pd.extracted_text,
    pd.rti_category,
    pd.rti_department,
    1 - (pd.embedding <=> query_embedding) as similarity
  FROM pdf_documents pd
  WHERE 1 - (pd.embedding <=> query_embedding) > match_threshold
  ORDER BY pd.embedding <=> query_embedding
  LIMIT match_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to search PDF documents by RTI category
CREATE OR REPLACE FUNCTION search_pdf_documents_by_category(category TEXT, department TEXT DEFAULT NULL)
RETURNS TABLE (
  id UUID,
  title TEXT,
  description TEXT,
  file_name TEXT,
  extracted_text TEXT,
  rti_category TEXT,
  rti_department TEXT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    pd.id,
    pd.title,
    pd.description,
    pd.file_name,
    pd.extracted_text,
    pd.rti_category,
    pd.rti_department
  FROM pdf_documents pd
  WHERE pd.rti_category = category
    AND (department IS NULL OR pd.rti_department = department)
  ORDER BY pd.created_at DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Note: Sample PDF documents will be uploaded through the API
-- The pdf_documents table is ready for storing PDF files with vector embeddings
