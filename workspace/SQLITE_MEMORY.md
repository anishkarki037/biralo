# SQLite Memory System Implementation

## Overview

Biralo now has a powerful SQLite-based memory system that dramatically improves upon the previous markdown-only approach. This provides structured storage, full-text search, categorization, and automatic consolidation.

## Key Improvements

### 1. **Full-Text Search**
- Search across all memories using FTS5 (Full-Text Search 5)
- Support for complex queries with boolean operators
- Automatic relevance ranking

```python
# Search memories
results = memory.search_memories(
    query="database optimization",
    category="project",
    min_importance=3,
    limit=10
)
```

### 2. **Categorization & Tags**
- Organize memories into categories (user-info, project, learning, etc.)
- Apply multiple tags to memories for flexible organization
- Filter memories by category or tags

```python
# Add memory with tags
mem_id = memory.add_memory(
    content="Important project update",
    category="project",
    importance=4,
    tags=["project-x", "urgent", "database"]
)

# Retrieve by category
memory.get_memories_by_category("project", days_back=30)

# Retrieve by tag
memory.get_memories_by_tag("urgent")
```

### 3. **Importance Levels**
- Prioritize memories (1-5 scale)
- Filter by importance threshold
- High-importance memories sorted first

```python
# Add high-priority memory
memory.add_memory(
    content="Critical system requirement",
    importance=5  # Highest priority
)

# Search with importance filter
results = memory.search_memories(query="system", min_importance=4)
```

### 4. **Automatic Consolidation**
- Identify high-value memories for long-term storage
- Automatically consolidate daily notes into structured knowledge
- Remove redundant information

```python
from biralo.agent.memory_consolidation import MemoryConsolidationService

consolidation = MemoryConsolidationService(workspace)

# Get consolidation report
report = consolidation.get_consolidation_report(days=7)

# Auto-consolidate high-importance memories
summary = consolidation.auto_consolidate(days=7, threshold=4)
```

### 5. **Memory Analytics**
- Track access statistics
- Monitor memory distribution
- Identify frequently used information

```python
# Get comprehensive statistics
stats = memory.get_memory_stats()
print(stats['total_memories'])
print(stats['by_category'])
print(stats['by_importance'])
print(stats['top_tags'])
```

### 6. **Access Tracking**
- Track when memories were last accessed
- Count how many times each memory is used
- Prioritize frequently-accessed memories

### 7. **Backward Compatibility**
- Daily markdown notes (YYYY-MM-DD.md) still work
- MEMORY.md continues to function
- Memories are stored in both formats for compatibility

## Architecture

### Database Schema

```
memories:
  - id (PRIMARY KEY)
  - content (TEXT)
  - category (TEXT)
  - importance (1-5)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
  - accessed_at (TIMESTAMP)
  - access_count (INTEGER)
  - source (TEXT, e.g., 'conversation', 'daily-note')
  - is_consolidated (BOOLEAN)
  - consolidation_note (TEXT)

memory_tags:
  - id (PRIMARY KEY)
  - memory_id (FOREIGN KEY)
  - tag (TEXT)

daily_notes:
  - id (PRIMARY KEY)
  - date (TEXT, e.g., '2025-02-12')
  - content (TEXT)

long_term_memory:
  - id (PRIMARY KEY)
  - section (TEXT)
  - content (TEXT)

memories_fts: (Virtual FTS5 table for full-text search)
```

## Core Components

### 1. **MemoryDatabase** (`memory_db.py`)
Low-level SQLite operations:
- Database initialization and schema management
- CRUD operations on memories
- Full-text search queries
- Metadata management
- Tag operations

### 2. **MemoryStore** (`memory.py`)
High-level memory API:
- Unified interface for markdown and SQLite
- Daily note management
- Long-term memory management
- Context building for LLM prompts
- Migration helpers

### 3. **MemoryMigration** (`memory_migration.py`)
One-time migration utilities:
- Import existing markdown memories
- Automatic section extraction
- Category inference
- Data validation

### 4. **MemoryConsolidationService** (`memory_consolidation.py`)
Automatic memory optimization:
- Consolidation candidate detection
- Similar memory grouping
- Auto-consolidation workflow
- Old memory archival
- Memory summaries

## Usage Examples

### Adding Memories from Conversations

```python
# Extract important information from conversation
memory.add_memory(
    content="User's project uses Node.js backend with PostgreSQL database",
    category="user-info",
    importance=4,
    tags=["tech-stack", "project-abc"],
    source="conversation"
)
```

### Searching for Context

```python
# Find all project-related memories
project_memories = memory.search_memories(
    query="project",
    tags=["project-abc"],
    min_importance=2,
    limit=20
)

# Use in system prompt
context = "\n".join([m['content'] for m in project_memories])
```

### Consolidating Daily Notes

```python
consolidation = MemoryConsolidationService(workspace)

# Get candidates for consolidation
candidates = memory.get_consolidation_candidates(days=7)

# Consolidate important learnings
for candidate in candidates:
    if candidate['importance'] >= 4:
        consolidation.consolidate_memories(
            [candidate['id']],
            section="Important-Learnings",
            consolidation_note="Extracted from daily notes"
        )
```

### Memory Analytics

```python
# Check memory health
stats = memory.get_memory_stats()

if stats['total_memories'] > 1000:
    # Cleanup old memories
    consolidation = MemoryConsolidationService(workspace)
    result = consolidation.cleanup_old_memories(days=90)
    print(f"Archived {result['memories_archived']} old memories")

# View most accessed memories
summary = consolidation.get_memory_summary(limit=10)
for mem in summary['top_memories']:
    print(f"Accessed {mem['access_count']} times: {mem['content']}")
```

## Migration Guide

### Automatic Migration

```python
from biralo.agent.memory_migration import MemoryMigration

migration = MemoryMigration(workspace)
results = migration.run_full_migration()

print(f"Migrated {results['daily_notes_migrated']} daily note files")
print(f"Migrated MEMORY.md: {results['long_term_migrated']}")
print(f"Total memories in database: {results['total_memories_in_db']}")
```

### Verify Migration

```python
verification = migration.verify_migration()
print(f"Total memories: {verification['total_memories']}")
print(f"Categories: {verification['categories']}")
print(f"Top tags: {verification['top_tags']}")
```

## Performance Characteristics

- **Search**: O(log n) with FTS5 indexing
- **Category filter**: O(log n) with index on category
- **Tag filter**: O(m) where m is number of tags (typically small)
- **Access stats**: O(1) update to counter

Database size: ~1KB per 50 memories (very efficient)

## Best Practices

### 1. **Use Meaningful Categories**
```python
# Good categories
"user-info", "project", "learning", "preferences", "important"

# Less specific (limit use)
"general", "misc"
```

### 2. **Apply Relevant Tags**
```python
# Good tagging strategy
memory.add_memory(
    content="...",
    tags=["project-name", "component-type", "priority-level"]
)
```

### 3. **Set Appropriate Importance**
```
5 - Critical system information (never forget)
4 - Important information (often needed)
3 - Regular information (useful)
2 - Historical information (might be relevant)
1 - Trivial information (reference only)
```

### 4. **Regular Consolidation**
- Run consolidation weekly
- Archive memories older than 90 days
- Keep active memories fresh and relevant

### 5. **Monitor Statistics**
```python
# Periodically check memory health
stats = memory.get_memory_stats()
if stats['total_memories'] > 2000:
    # Time to consolidate and archive
    pass
```

## Integration with Agent Loop

The memory system is automatically integrated into the agent loop:

```python
# In ContextBuilder.build_system_prompt()
memory_context = self.memory.get_memory_context()  # Uses SQLite + markdown
```

## Troubleshooting

### Database Corruption

```python
# Reset database (destructive)
from pathlib import Path
db_path = workspace / "memory" / "memories.db"
db_path.unlink()  # Delete
# Will be recreated on next use
```

### Search Not Finding Results

```python
# Check if memory exists
stats = memory.get_memory_stats()
print(stats['total_memories'])

# Verify search query syntax (FTS5)
# Use quotes for exact phrases: "exact phrase"
# Use AND/OR/NOT for boolean: "term1 AND term2"
```

### Memory Growth

```python
# Monitor and cleanup
stats = memory.get_memory_stats()
print(f"Total: {stats['total_memories']}")

# Consolidate high-importance
consolidation = MemoryConsolidationService(workspace)
consolidation.auto_consolidate(threshold=4)

# Archive old
consolidation.cleanup_old_memories(days=90)
```

## Future Enhancements

Potential future improvements:
- Semantic similarity search with embeddings
- Memory graph visualization
- Topic model extraction
- Automatic summarization
- Backup and sync capabilities
- Memory privacy controls
- External knowledge base integration
