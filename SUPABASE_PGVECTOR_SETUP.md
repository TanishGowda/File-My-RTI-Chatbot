# Supabase pgvector Setup Guide

## The Issue
You're getting the error because the `pgvector` extension is not enabled in your Supabase project. This is a common issue as pgvector needs to be manually enabled.

## Solution 1: Enable pgvector in Supabase (Recommended)

### Step 1: Enable pgvector Extension
1. Go to your Supabase project dashboard
2. Navigate to **Database** → **Extensions**
3. Search for "pgvector" or "vector"
4. Click **Enable** next to the pgvector extension
5. Wait for it to be enabled (may take a few minutes)

### Step 2: Update the Schema
Once pgvector is enabled, run this updated schema:

```sql
-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- Update knowledge base table to use proper vector type
ALTER TABLE knowledge_base ALTER COLUMN embedding TYPE VECTOR(1536);

-- Create vector index
CREATE INDEX idx_knowledge_base_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops);

-- Replace the text-based search function with vector-based search
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
```

### Step 3: Update Python Backend
If you enable pgvector, you'll need to update the Python backend to use vector embeddings again:

```python
# In backend/app/services/supabase_client.py
async def search_knowledge_base(self, query_embedding: List[float], threshold: float = None, limit: int = None) -> List[Dict[str, Any]]:
    """Search knowledge base using vector similarity"""
    try:
        response = self.client.rpc("search_knowledge_base", {
            "query_embedding": query_embedding,
            "match_threshold": threshold or settings.RAG_SIMILARITY_THRESHOLD,
            "match_count": limit or settings.RAG_MAX_RESULTS
        }).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error searching knowledge base: {e}")
        return []
```

## Solution 2: Use Text-Based Similarity (Current Implementation)

The current implementation I provided uses PostgreSQL's built-in `similarity()` function, which works without pgvector. This is a good fallback solution.

### How it works:
- Uses PostgreSQL's `pg_trgm` extension (usually enabled by default)
- Performs text similarity matching instead of vector similarity
- Still provides good results for RTI-related queries

### To use this approach:
1. Run the current schema as-is (it's already configured for text similarity)
2. The Python backend is already updated to work with text search
3. No additional configuration needed

## Solution 3: Hybrid Approach

You can use both approaches:

1. **For now**: Use text-based similarity (current implementation)
2. **Later**: Enable pgvector and switch to vector-based search for better results

## Testing the Setup

### Test Text-Based Search
```sql
-- Test the text-based search function
SELECT * FROM search_knowledge_base('RTI application format', 0.3, 3);
```

### Test Vector-Based Search (after enabling pgvector)
```sql
-- Test with a sample embedding (you'd normally get this from OpenAI)
SELECT * FROM search_knowledge_base('[0.1, 0.2, 0.3, ...]'::vector, 0.5, 3);
```

## Performance Comparison

| Method | Pros | Cons |
|--------|------|------|
| **Text Similarity** | ✅ Works immediately<br>✅ No additional setup<br>✅ Good for RTI content | ❌ Less accurate than vectors<br>❌ Slower for large datasets |
| **Vector Similarity** | ✅ More accurate<br>✅ Better semantic understanding<br>✅ Faster for large datasets | ❌ Requires pgvector setup<br>❌ More complex |

## Recommendation

For the FileMyRTI project:

1. **Start with text similarity** (current implementation) - it works immediately
2. **Enable pgvector later** when you want better search accuracy
3. **The current setup is production-ready** and will work well for RTI queries

## Next Steps

1. **Run the current schema** - it will work with text similarity
2. **Test the application** - everything should work fine
3. **Consider enabling pgvector later** for better search results
4. **Monitor performance** and decide if you need vector search

The text-based approach is actually quite good for RTI content since it's mostly structured text with specific terminology that works well with text similarity matching.
