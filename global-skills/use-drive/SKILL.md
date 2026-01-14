---
name: use-drive
description: Interact with Google Drive API via CLI scripts. Upload, download, list, search, share, and manage files and folders.
---

# use-drive

CLI tools for interacting with Google Drive API.

## When to Use

Use this skill when you need to:
- Upload files to Google Drive
- Download files from Google Drive
- List files in a folder
- Search for files
- Create folders
- Move, copy, or delete files
- Share files with other users
- Get file metadata

## Requirements

Install dependencies:

```bash
pip install -r .claude/new-skills/use-drive/requirements.txt
```

Credentials are expected at:
- `MCP_servers/google-credentials/credentials.json` (OAuth client)
- Token will be saved at `MCP_servers/google-credentials/token-drive.json`

## Available Scripts

All scripts are in `.claude/new-skills/use-drive/scripts/`.

### upload_file.py - Upload a file

```bash
python scripts/upload_file.py --file-path /path/to/file.pdf
python scripts/upload_file.py --file-path /path/to/file.pdf --name "Renamed.pdf"
python scripts/upload_file.py --file-path /path/to/file.pdf --parent-id FOLDER_ID
```

**Arguments:**
- `--file-path` (required): Local file path to upload
- `--name`: Name for the file in Drive (defaults to filename)
- `--parent-id`: Parent folder ID (defaults to root)
- `--mime-type`: MIME type (auto-detected if not provided)

**Output:** JSON with uploaded file info (id, name, mimeType, webViewLink, etc.)

### download_file.py - Download a file

```bash
python scripts/download_file.py --file-id FILE_ID --output-path ./downloaded.pdf
```

**Arguments:**
- `--file-id` (required): ID of the file to download
- `--output-path` (required): Local path to save the file

**Output:** JSON with download info (file_id, name, output_path, size)

### list_files.py - List files in a folder

```bash
python scripts/list_files.py
python scripts/list_files.py --parent-id FOLDER_ID
python scripts/list_files.py --max-results 50
python scripts/list_files.py --mime-type application/pdf
```

**Arguments:**
- `--parent-id`: Parent folder ID (lists all files if not specified)
- `--max-results`: Maximum number of results (1-1000, default: 100)
- `--mime-type`: Filter by MIME type
- `--order-by`: Sort order (default: 'modifiedTime desc')

**Output:** JSON array of files

### search_files.py - Search for files

```bash
python scripts/search_files.py --query "name contains 'report'"
python scripts/search_files.py --query "mimeType='application/pdf'"
python scripts/search_files.py --query "fullText contains 'budget'"
```

**Arguments:**
- `--query` (required): Search query using Drive search operators
- `--max-results`: Maximum number of results (1-1000, default: 100)

**Query Examples:**
- `name contains 'report'`
- `mimeType='application/pdf'`
- `fullText contains 'budget'`
- `'FOLDER_ID' in parents`
- `modifiedTime > '2024-01-01'`

**Output:** JSON array of matching files

### create_folder.py - Create a folder

```bash
python scripts/create_folder.py --name "My New Folder"
python scripts/create_folder.py --name "Subfolder" --parent-id FOLDER_ID
```

**Arguments:**
- `--name` (required): Name of the folder to create
- `--parent-id`: Parent folder ID (defaults to root)

**Output:** JSON with created folder info (id, name, webViewLink)

### move_file.py - Move a file

```bash
python scripts/move_file.py --file-id FILE_ID --new-parent-id FOLDER_ID
```

**Arguments:**
- `--file-id` (required): ID of the file to move
- `--new-parent-id` (required): ID of the new parent folder

**Output:** JSON with moved file info

### copy_file.py - Copy a file

```bash
python scripts/copy_file.py --file-id FILE_ID
python scripts/copy_file.py --file-id FILE_ID --new-name "Copy of Document.pdf"
python scripts/copy_file.py --file-id FILE_ID --parent-id FOLDER_ID
```

**Arguments:**
- `--file-id` (required): ID of the file to copy
- `--new-name`: Name for the copy (defaults to 'Copy of [original]')
- `--parent-id`: Parent folder for the copy

**Output:** JSON with copied file info

### delete_file.py - Delete a file

```bash
python scripts/delete_file.py --file-id FILE_ID
```

**Arguments:**
- `--file-id` (required): ID of the file to delete

**Output:** JSON with deletion status

Note: File is moved to trash, not permanently deleted.

### share_file.py - Share a file

```bash
# Share with a specific user
python scripts/share_file.py --file-id FILE_ID --email user@example.com --role reader
python scripts/share_file.py --file-id FILE_ID --email user@example.com --role writer

# Share with anyone (public link)
python scripts/share_file.py --file-id FILE_ID --role reader --type anyone
```

**Arguments:**
- `--file-id` (required): ID of the file to share
- `--email`: Email address (required for user/group type)
- `--role` (required): Permission role (reader, writer, commenter, owner)
- `--type`: Permission type (user, group, domain, anyone; default: user)

**Output:** JSON with permission info and shareable link

### get_file_info.py - Get file information

```bash
python scripts/get_file_info.py --file-id FILE_ID
python scripts/get_file_info.py --file-id FILE_ID --fields "id,name,size,mimeType"
```

**Arguments:**
- `--file-id` (required): ID of the file
- `--fields`: Comma-separated fields to retrieve (default: all)

**Output:** JSON with file metadata

## Error Handling

All scripts output errors as JSON:

```json
{"error": "Error message here"}
```

Exit code is 1 on error, 0 on success.

## Common Arguments

All scripts accept:
- `--credentials-path`: Path to OAuth credentials JSON file
- `--token-path`: Path to user token file

## Common MIME Types

| Type | MIME Type |
|------|-----------|
| Folder | `application/vnd.google-apps.folder` |
| Google Doc | `application/vnd.google-apps.document` |
| Google Sheet | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `application/vnd.google-apps.presentation` |
| PDF | `application/pdf` |
| Text | `text/plain` |
| Image | `image/jpeg`, `image/png`, etc. |
