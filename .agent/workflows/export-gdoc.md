---
description: Export a markdown file to .docx for clean Google Docs import
---

# Export Markdown to Google Docs (.docx)

Converts any markdown file to a properly styled `.docx` using Pandoc. Handles legal agreements, content packs, proposals, and any structured markdown.

## Steps

// turbo
1. Run the export script:
```bash
.agent/scripts/md-to-docx.sh "<path-to-markdown-file>"
```

The script will:
- Apply the reference template for consistent styling (headings, tables, spacing)
- Run the Lua filter to fix common issues (dual H1s, horizontal rules, escaped chars)
- Output a `.docx` file in the same directory as the input

2. Report the output file path and size to the user.

3. Suggest: "Upload to Google Drive or open locally with `open <output.docx>`"

## Notes

- The reference template is at `.agent/scripts/reference.docx`
- The Lua filter is at `.agent/scripts/legal-filter.lua`
- To specify a custom output path: `.agent/scripts/md-to-docx.sh input.md /path/to/output.docx`
- Works on any markdown file in any workspace
