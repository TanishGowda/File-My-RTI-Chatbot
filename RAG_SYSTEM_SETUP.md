# PDF-Based RAG System Setup Guide

## 🎯 Overview
Your chatbot now has a complete PDF-based RAG (Retrieval-Augmented Generation) system that can:
- Store PDF documents with vector embeddings
- Search for relevant RTI format templates
- Generate RTI applications using PDF templates
- Provide enhanced responses with PDF context

## 📋 Prerequisites

### 1. Enable pgvector in Supabase
1. Go to your Supabase project dashboard
2. Navigate to **Database** → **Extensions**
3. Search for "pgvector" and click **Enable**
4. Wait for it to be enabled (may take a few minutes)

### 2. Run Database Migration
1. Go to **SQL Editor** in Supabase
2. Copy and paste the contents of `supabase/migration_to_pdf_rag.sql`
3. Click **Run** to execute the migration
4. This will:
   - Delete the old `knowledge_base` table
   - Create the new `pdf_documents` table
   - Set up vector search functions
   - Add sample RTI format templates

## 🚀 New Features

### 1. PDF Upload Endpoint
**POST** `/api/v1/chat/upload-pdf`

Upload PDF documents to the knowledge base:
```bash
curl -X POST "http://localhost:8000/api/v1/chat/upload-pdf" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@rti_format.pdf" \
  -F "title=Land Records RTI Format" \
  -F "description=Standard format for land records applications" \
  -F "rti_category=land_records" \
  -F "rti_department=Land Records Department"
```

### 2. Enhanced Chat with RAG
The chat endpoint now automatically uses PDF-based RAG:
- Searches for relevant RTI format templates
- Uses vector similarity to find the best match
- Generates responses with PDF context

### 3. RTI Draft Generation
**POST** `/api/v1/chat/generate-rti-draft`

Generate RTI applications using PDF templates:
```bash
curl -X POST "http://localhost:8000/api/v1/chat/generate-rti-draft" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to file an RTI for land records", "conversation_id": "uuid"}'
```

## 📊 Database Schema

### pdf_documents Table
```sql
CREATE TABLE pdf_documents (
  id UUID PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  file_name TEXT NOT NULL,
  file_data BYTEA NOT NULL,           -- PDF file content
  file_size INTEGER NOT NULL,
  file_type TEXT DEFAULT 'application/pdf',
  extracted_text TEXT NOT NULL,       -- Extracted text for search
  embedding VECTOR(1536),             -- Vector embedding for similarity
  rti_category TEXT,                  -- Category like 'land_records', 'employment'
  rti_department TEXT,                -- Specific department
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🔧 How It Works

### 1. PDF Upload Process
1. User uploads PDF file
2. System extracts text using PyPDF2
3. Generates vector embedding using OpenAI
4. Stores PDF + text + embedding in database

### 2. RAG Query Process
1. User asks a question
2. System generates embedding for the query
3. Searches PDF documents using vector similarity
4. Retrieves relevant RTI format templates
5. Uses templates to generate enhanced response

### 3. RTI Draft Generation
1. User requests RTI application
2. System finds relevant PDF format template
3. Uses template structure to generate application
4. Fills in user-specific information

## 📝 RTI Categories

Suggested categories for organizing PDF templates:
- `land_records` - Land and property related RTIs
- `employment` - Employment and recruitment RTIs
- `education` - Educational institution RTIs
- `health` - Healthcare and medical RTIs
- `finance` - Financial and tax related RTIs
- `legal` - Legal and court related RTIs
- `general` - General purpose RTI formats

## 🧪 Testing the System

### 1. Upload a Sample PDF
```bash
# Create a sample RTI format PDF and upload it
curl -X POST "http://localhost:8000/api/v1/chat/upload-pdf" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@sample_rti_format.pdf" \
  -F "title=Sample RTI Format" \
  -F "rti_category=general"
```

### 2. Test RAG Chat
```bash
# Ask a question that should use the PDF context
curl -X POST "http://localhost:8000/api/v1/chat/send-message" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I file an RTI for land records?", "conversation_id": "uuid"}'
```

### 3. Generate RTI Draft
```bash
# Generate an RTI application using PDF templates
curl -X POST "http://localhost:8000/api/v1/chat/generate-rti-draft" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "I need to file an RTI for employment records", "conversation_id": "uuid"}'
```

## 🔍 Vector Search Functions

### search_pdf_documents
Searches PDF documents using vector similarity:
```sql
SELECT * FROM search_pdf_documents('[0.1,0.2,0.3]'::vector, 0.5, 5);
```

### search_pdf_documents_by_category
Searches by RTI category:
```sql
SELECT * FROM search_pdf_documents_by_category('land_records', 'Land Records Department');
```

## ⚠️ Important Notes

1. **pgvector Required**: The system requires pgvector extension for vector similarity search
2. **File Size Limits**: Consider file size limits for PDF uploads
3. **Text Extraction**: PDFs must contain readable text (not scanned images)
4. **Embedding Costs**: Each PDF upload generates embeddings (costs OpenAI credits)
5. **Vector Index**: The system creates a vector index for fast similarity search

## 🎉 Benefits

1. **Accurate RTI Formats**: Uses actual PDF templates for RTI applications
2. **Semantic Search**: Finds relevant templates even with different wording
3. **Scalable**: Can handle thousands of PDF documents
4. **Context-Aware**: Responses include relevant PDF context
5. **Template-Based**: Generates RTI applications using proper formats

## 🚀 Next Steps

1. **Upload PDF Templates**: Add your RTI format PDFs to the system
2. **Test Chat**: Try asking RTI-related questions
3. **Generate Drafts**: Test the RTI draft generation
4. **Monitor Performance**: Check vector search performance
5. **Add More Categories**: Expand with more RTI categories

Your RAG system is now ready to provide intelligent, PDF-based RTI assistance! 🎯
