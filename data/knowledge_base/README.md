# Serendib Routes RAG Knowledge Base v3

This package is a cleaned replacement knowledge base designed to improve retrieval and grounding.

## Key fixes
- Split hotel references by region to prevent Ella/coast mixups.
- Removed claims that hotel licences, operating status, rates, or availability are verified.
- Added explicit live-data boundaries.
- Separated **6 nights / 7 days** from **7 nights / 8 days**.
- Added a dedicated **Making a Trip More Affordable** chunk so queries like "Can you make it cheaper?" retrieve relevant guidance.
- Kept budget examples duration-specific and prohibited multiplying them into new totals.
- Added titles and descriptive text into each chunk for better semantic retrieval.
- Added metadata for category, region, intent tags, dynamic status, and stability.

## Files
- `rag_chunks.jsonl` — consolidated ingestion file.
- `source_docs/` — one Markdown file per chunk for easy editing.
- `manifest.json` — chunk list and metadata.
- `REINGEST_STEPS.txt` — replacement/re-ingestion checklist.

## Compatibility
Each JSONL line includes `chunk_id`, `title`, `content`, `text`, `page_content`, and `metadata`. The duplicate text fields are intentional so the file is easy to adapt to common LangChain loaders. Use whichever field your `DocumentManager` currently reads.

## Important
This is a reconstructed and cleaned version based on the Serendib Routes material and retrieval logs available in the conversation. Dynamic hotel, visa, weather, schedule, pricing, and availability claims must still be verified live before production use.
