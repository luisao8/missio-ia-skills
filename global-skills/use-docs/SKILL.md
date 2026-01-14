---
name: use-docs
description: Interact with Google Docs API to create, read, update, and export documents via CLI scripts.
---

# use-docs Skill

This skill provides CLI scripts to interact with Google Docs API. Use these scripts to manage Google Docs programmatically.

## When to Use This Skill

- Creating new Google Docs with optional initial content
- Reading the content of existing documents
- Updating or replacing document content
- Appending or inserting text at specific positions
- Finding and replacing text across a document
- Exporting documents to PDF, DOCX, TXT, or HTML
- Getting metadata about documents

## Prerequisites

1. Google OAuth credentials must be set up in `MCP_servers/google-credentials/credentials.json`
2. Required Python packages installed (see `requirements.txt`)

## Available Scripts

All scripts are located in `scripts/` and output JSON.

### create_doc.py - Create a New Document

```bash
# Create a simple document
python scripts/create_doc.py --title "Meeting Notes"

# Create with initial content
python scripts/create_doc.py --title "Report" --content "# Quarterly Report\n\nContent here..."

# Create in a specific folder
python scripts/create_doc.py --title "Project Doc" --folder-id "1abc123xyz"
```

### read_doc.py - Read Document Content

```bash
# Read document content
python scripts/read_doc.py --doc-id "1abc123xyz789"
```

**Output includes:** id, title, content, content_length, revision_id

### update_doc.py - Replace All Content

```bash
# Replace all document content
python scripts/update_doc.py --doc-id "1abc123xyz" --content "New document content"
```

**Warning:** This replaces ALL existing content. Use `append_text.py` or `insert_text.py` to add without replacing.

### append_text.py - Add Text to End

```bash
# Append text to the end of a document
python scripts/append_text.py --doc-id "1abc123xyz" --text "\n\nNew section at the end"
```

### insert_text.py - Insert at Position

```bash
# Insert at the beginning (index 1)
python scripts/insert_text.py --doc-id "1abc123xyz" --text "Title: " --index 1

# Insert at a specific position
python scripts/insert_text.py --doc-id "1abc123xyz" --text "[INSERTED]" --index 50
```

**Note:** Index 1 is the start of the document.

### replace_text.py - Find and Replace

```bash
# Replace all occurrences (case-insensitive)
python scripts/replace_text.py --doc-id "1abc123xyz" --find "TODO" --replace "DONE"

# Case-sensitive replacement
python scripts/replace_text.py --doc-id "1abc123xyz" --find "Name" --replace "Title" --match-case
```

### export_doc.py - Export to Other Formats

```bash
# Export to PDF
python scripts/export_doc.py --doc-id "1abc123xyz" --format pdf

# Export to DOCX with custom path
python scripts/export_doc.py --doc-id "1abc123xyz" --format docx --output-path ./report.docx

# Export to plain text
python scripts/export_doc.py --doc-id "1abc123xyz" --format txt

# Export to HTML
python scripts/export_doc.py --doc-id "1abc123xyz" --format html
```

**Supported formats:** pdf, docx, txt, html

### get_doc_info.py - Get Document Metadata

```bash
# Get document info
python scripts/get_doc_info.py --doc-id "1abc123xyz"
```

**Output includes:** id, title, character_count, revision_id, link, created_time, modified_time, owners

## Common Options

All scripts support these optional arguments:

- `--credentials-path`: Path to directory containing `credentials.json` (defaults to `MCP_servers/google-credentials/`)
- `--help`: Show help message and usage examples

## Output Format

All scripts output JSON to stdout:

**Success:**
```json
{
  "id": "1abc123xyz",
  "title": "Document Title",
  ...
}
```

**Error:**
```json
{
  "error": "Error message describing what went wrong"
}
```

## Finding Document IDs

The document ID is found in the Google Docs URL:
```
https://docs.google.com/document/d/DOCUMENT_ID/edit
                                   ^^^^^^^^^^^
```

## Example Workflow

```bash
# 1. Create a new document
python scripts/create_doc.py --title "Project Notes"
# Returns: {"id": "1abc...", "title": "Project Notes", "link": "..."}

# 2. Read it back
python scripts/read_doc.py --doc-id "1abc..."

# 3. Append some content
python scripts/append_text.py --doc-id "1abc..." --text "\n## Meeting Notes\n- Item 1\n- Item 2"

# 4. Replace a placeholder
python scripts/replace_text.py --doc-id "1abc..." --find "Item 1" --replace "First task completed"

# 5. Export to PDF
python scripts/export_doc.py --doc-id "1abc..." --format pdf --output-path ./project-notes.pdf

# 6. Get final document info
python scripts/get_doc_info.py --doc-id "1abc..."
```
