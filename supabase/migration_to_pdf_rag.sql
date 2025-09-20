-- Migration script to convert from knowledge_base to pdf_documents table
-- Run this script in your Supabase SQL editor

-- Step 1: Drop the old knowledge_base table and related functions
DROP TABLE IF EXISTS knowledge_base CASCADE;
DROP FUNCTION IF EXISTS search_knowledge_base(TEXT, FLOAT, INT) CASCADE;

-- Step 2: Create the new pdf_documents table
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

-- Step 3: Create indexes for better performance
CREATE INDEX idx_pdf_documents_rti_category ON pdf_documents(rti_category);
CREATE INDEX idx_pdf_documents_rti_department ON pdf_documents(rti_department);
-- Vector index for semantic search
CREATE INDEX idx_pdf_documents_embedding ON pdf_documents USING ivfflat (embedding vector_cosine_ops);

-- Step 4: Create updated_at trigger
CREATE TRIGGER update_pdf_documents_updated_at BEFORE UPDATE ON pdf_documents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Step 5: Enable RLS
ALTER TABLE pdf_documents ENABLE ROW LEVEL SECURITY;

-- Step 6: Create RLS policy
CREATE POLICY "PDF documents are publicly readable" ON pdf_documents FOR SELECT USING (true);

-- Step 7: Create search functions
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

-- Step 8: Sample data will be uploaded through the API
-- The pdf_documents table is ready for storing PDF files with vector embeddings
-- Upload your RTI format PDFs using the /upload-pdf endpoint

-- Migration completed successfully!
-- You can now upload PDF documents through the /upload-pdf endpoint
