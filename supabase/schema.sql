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

-- Create knowledge base table for RAG
CREATE TABLE knowledge_base (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  source_url TEXT,
  category TEXT,
  embedding TEXT, -- Store as JSON string for now (will be VECTOR(1536) when pgvector is enabled)
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
CREATE INDEX idx_knowledge_base_category ON knowledge_base(category);
-- Vector index will be created after pgvector is enabled
-- CREATE INDEX idx_knowledge_base_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops);

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
CREATE TRIGGER update_knowledge_base_updated_at BEFORE UPDATE ON knowledge_base FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE rti_drafts ENABLE ROW LEVEL SECURITY;
ALTER TABLE rti_filings ENABLE ROW LEVEL SECURITY;

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

-- Knowledge base is public read-only
CREATE POLICY "Knowledge base is publicly readable" ON knowledge_base FOR SELECT USING (true);

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

-- Function to search knowledge base using text similarity (temporary until pgvector is enabled)
CREATE OR REPLACE FUNCTION search_knowledge_base(query_text TEXT, match_threshold FLOAT DEFAULT 0.5, match_count INT DEFAULT 5)
RETURNS TABLE (
  id UUID,
  title TEXT,
  content TEXT,
  source_url TEXT,
  category TEXT,
  similarity FLOAT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    kb.id,
    kb.title,
    kb.content,
    kb.source_url,
    kb.category,
    similarity(kb.title || ' ' || kb.content, query_text) as similarity
  FROM knowledge_base kb
  WHERE similarity(kb.title || ' ' || kb.content, query_text) > match_threshold
  ORDER BY similarity DESC
  LIMIT match_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Note: This function uses PostgreSQL's built-in similarity() function
-- For better vector search, enable pgvector and use the vector-based function below:

/*
-- Vector-based search function (use after enabling pgvector)
CREATE OR REPLACE FUNCTION search_knowledge_base(query_embedding VECTOR(1536), match_threshold FLOAT DEFAULT 0.5, match_count INT DEFAULT 5)
RETURNS TABLE (
  id UUID,
  title TEXT,
  content TEXT,
  source_url TEXT,
  category TEXT,
  similarity FLOAT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    kb.id,
    kb.title,
    kb.content,
    kb.source_url,
    kb.category,
    1 - (kb.embedding <=> query_embedding) as similarity
  FROM knowledge_base kb
  WHERE 1 - (kb.embedding <=> query_embedding) > match_threshold
  ORDER BY kb.embedding <=> query_embedding
  LIMIT match_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
*/

-- Insert sample knowledge base data
INSERT INTO knowledge_base (title, content, category, source_url) VALUES
('RTI Act 2005 Overview', 'The Right to Information Act, 2005 is an Act of the Parliament of India "to provide for setting out the practical regime of right to information for citizens" to secure access to information under the control of public authorities.', 'legal', 'https://rti.gov.in/'),
('RTI Application Format', 'RTI applications should be submitted in writing or through electronic means in English, Hindi or in the official language of the area in which the application is being made.', 'procedure', 'https://rti.gov.in/'),
('RTI Fees and Charges', 'RTI applications require a fee of Rs. 10/- for Central Government departments. State governments may have different fee structures.', 'fees', 'https://rti.gov.in/'),
('RTI Exemptions', 'Information that would prejudicially affect the sovereignty and integrity of India, security, strategic, scientific or economic interests of the State, or information received in confidence from foreign government is exempted.', 'exemptions', 'https://rti.gov.in/'),
('RTI Appeal Process', 'If an RTI application is rejected or information is not provided, citizens can file a first appeal to the First Appellate Authority within 30 days.', 'appeals', 'https://rti.gov.in/');
