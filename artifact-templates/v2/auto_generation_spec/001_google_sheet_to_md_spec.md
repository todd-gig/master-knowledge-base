---
title: Google Sheets to MD Auto Generation Spec
tags: [automation, sheets, md]
---

# Google Sheets → Markdown Auto Generation

## Objective
Convert structured rows into standardized MD artifacts.

## Input Mapping

### Sheet: Master_Catalog
| Column | MD Field |
|--------|----------|
| Name | Artifact Name |
| Category | Category |
| Description | Description |
| Primary_Goal | Goal |
| Channels | Where |

## Conversion Rules
- Each row = 1 MD file
- File name = slug(Name)
- Use universal template
- Inject fields into sections

## Example Pseudocode (Python)

```python
def row_to_md(row):
    return f"""
# {row['Name']}

## Goal
{row['Primary_Goal']}

## Description
{row['Description']}
"""
```

## Output Structure
- /generated_md/
  - artifact_001.md
  - artifact_002.md

## Extensions
- Batch processing
- Sync back to Google Drive
- Version tracking
