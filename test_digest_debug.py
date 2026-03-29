#!/usr/bin/env python3
"""Debug script to test digest generation."""
import sys
from pathlib import Path
from config import Settings
from src.database.vector_db import VectorDatabase

settings = Settings()

print("🔍 Digest Debug Test\n")
print("="*60)

# 1. Check database
print("\n1️⃣  Checking database...")
vector_db = VectorDatabase(
    db_path=settings.chroma_db_path,
    embedding_model=settings.embedding_model,
    chunk_size=settings.chunk_size,
    chunk_overlap=settings.chunk_overlap,
)

stats = vector_db.get_stats()
print(f"   Total documents: {stats['total_documents']}")
print(f"   Total chunks: {stats['total_chunks']}")

if stats['total_documents'] == 0:
    print("   ❌ Database is empty! Run 'python main.py update' first")
    sys.exit(1)

# 2. Check document structure
print("\n2️⃣  Checking document structure...")
all_data = vector_db.collection.get(limit=1, include=["metadatas", "documents"])
if all_data and all_data.get("metadatas"):
    sample_doc = all_data["metadatas"][0]
    sample_content = all_data["documents"][0] if all_data.get("documents") else ""

    print(f"   Sample document keys: {list(sample_doc.keys())}")
    print(f"   - Title: {sample_doc.get('title', 'N/A')[:60]}...")
    print(f"   - Source: {sample_doc.get('source', 'N/A')}")
    print(f"   - Has abstract in metadata: {'abstract' in sample_doc}")
    print(f"   - Content (chunk) length: {len(sample_content)} chars")
    print(f"   - Content preview: {sample_content[:100]}...")

# 3. Test getting full database with abstracts
print("\n3️⃣  Testing full database retrieval...")
all_data = vector_db.collection.get(include=["metadatas", "documents"])

# Group chunks by doc_id (FIXED VERSION)
doc_chunks = {}
for i, metadata in enumerate(all_data["metadatas"]):
    doc_id = metadata.get("doc_id")
    if doc_id:
        if doc_id not in doc_chunks:
            doc_chunks[doc_id] = {
                "metadata": metadata,
                "chunks": []
            }
        if i < len(all_data["documents"]):
            chunk_index = metadata.get("chunk_index", 0)
            doc_chunks[doc_id]["chunks"].append((chunk_index, all_data["documents"][i]))

# Process each document
seen_doc_ids = {}
competitor_doc_ids = {}

for doc_id, data in doc_chunks.items():
    metadata = data["metadata"]
    source = metadata.get("source", "")
    is_competitor = source.startswith("competitor_")

    # Sort chunks by index and join them
    sorted_chunks = sorted(data["chunks"], key=lambda x: x[0])
    full_content = "\n\n".join([chunk for _, chunk in sorted_chunks])

    # Extract abstract from full content
    title = metadata.get("title", "")
    if full_content.startswith(title):
        abstract = full_content[len(title):].strip()
    else:
        abstract = full_content

    metadata["abstract"] = abstract[:500] if abstract else "No summary available"

    if is_competitor:
        competitor_doc_ids[doc_id] = metadata
    else:
        seen_doc_ids[doc_id] = metadata

docs_to_add = list(seen_doc_ids.values())
competitor_docs = list(competitor_doc_ids.values())

print(f"   ✓ Found {len(docs_to_add)} regular documents")
print(f"   ✓ Found {len(competitor_docs)} competitor documents")

# 4. Check if abstracts are populated
print("\n4️⃣  Checking abstracts...")
docs_with_abstract = sum(1 for doc in docs_to_add if doc.get("abstract") and doc["abstract"] != "No summary available")
print(f"   Documents with abstract: {docs_with_abstract}/{len(docs_to_add)}")

if docs_with_abstract < len(docs_to_add):
    print(f"   ⚠️  {len(docs_to_add) - docs_with_abstract} documents have no abstract")
    # Show sample
    for doc in docs_to_add[:3]:
        abstract = doc.get("abstract", "")
        print(f"   - {doc.get('title', '')[:50]}: abstract length = {len(abstract)} chars")

# 5. Test LLM summary generation
print("\n5️⃣  Testing LLM summary generation...")
from src.rag.generator import Generator

generator = Generator(
    provider=settings.llm_provider,
    api_key=settings.api_key,
    model=settings.llm_model,
    temperature=settings.llm_temperature,
    base_url=settings.llm_base_url,
)

if docs_to_add:
    test_doc = docs_to_add[0]
    print(f"   Testing with: {test_doc.get('title', '')[:60]}...")

    try:
        # Get full content
        doc_id = test_doc.get("doc_id")
        chunks_data = vector_db.collection.get(
            where={"doc_id": doc_id},
            include=["documents"]
        )
        if chunks_data and chunks_data.get("documents"):
            full_content = "\n\n".join(chunks_data["documents"])
            summary = generator.generate_article_summary(
                title=test_doc.get("title", ""),
                content=full_content
            )
            print(f"   ✓ Generated summary: {summary}")
        else:
            print(f"   ✗ No chunks found for doc_id={doc_id}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

print("\n" + "="*60)
print("✅ Debug test complete!")
print("\nNext steps:")
print("  1. If database is empty → python main.py update")
print("  2. If LLM fails → check Ollama is running (ollama serve)")
print("  3. Run digest → python main.py digest --full-database --preview")
