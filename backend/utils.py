import json
import re
import logging
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def json_table_to_markdown(json_data: Dict) -> str:
    """Convert JSON table format to markdown table"""
    try:
        headers = json_data.get("headers", [])
        rows = json_data.get("rows", [])
        
        if not headers:
            return ""
        
        # Build markdown table
        markdown_lines = []
        
        # Header row
        header_row = "| " + " | ".join(str(h) for h in headers) + " |"
        markdown_lines.append(header_row)
        
        # Separator row
        separator = "| " + " | ".join(["---"] * len(headers)) + " |"
        markdown_lines.append(separator)
        
        # Data rows
        for row in rows:
            # Ensure row has same number of columns as headers
            row_data = row if isinstance(row, list) else [row]
            # Pad or truncate to match header count
            while len(row_data) < len(headers):
                row_data.append("")
            row_data = row_data[:len(headers)]
            
            row_markdown = "| " + " | ".join(str(cell) for cell in row_data) + " |"
            markdown_lines.append(row_markdown)
        
        return "\n".join(markdown_lines)
    except Exception as e:
        logger.error(f"Error converting JSON table to markdown: {str(e)}")
        return ""


def extract_and_convert_json_tables(text: str) -> str:
    """Extract JSON tables from text and convert them to markdown"""
    try:
        # Look for JSON tables in code blocks
        # Pattern 1: ```table_json\n{...}\n```
        json_block_pattern = r'```table_json\s*\n(.*?)\n```'
        matches = list(re.finditer(json_block_pattern, text, re.DOTALL))
        
        for match in reversed(matches):  # Reverse to maintain positions
            json_str = match.group(1).strip()
            try:
                json_data = json.loads(json_str)
                markdown_table = json_table_to_markdown(json_data)
                if markdown_table:
                    # Replace the JSON block with markdown table
                    text = text[:match.start()] + markdown_table + text[match.end():]
                    logger.info("Converted JSON table to markdown")
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON table: {str(e)}")
                continue
        
        # Pattern 2: Look for standalone JSON objects that look like tables
        # This is more lenient - looks for { "headers": [...], "rows": [...] }
        json_object_pattern = r'\{[^{}]*"headers"\s*:\s*\[[^\]]+\][^{}]*"rows"\s*:\s*\[[^\]]+\][^{}]*\}'
        matches = list(re.finditer(json_object_pattern, text, re.DOTALL))
        
        for match in reversed(matches):
            json_str = match.group(0)
            try:
                json_data = json.loads(json_str)
                if "headers" in json_data and "rows" in json_data:
                    markdown_table = json_table_to_markdown(json_data)
                    if markdown_table:
                        text = text[:match.start()] + markdown_table + text[match.end():]
                        logger.info("Converted standalone JSON table to markdown")
            except json.JSONDecodeError:
                continue
        
        return text
    except Exception as e:
        logger.error(f"Error extracting JSON tables: {str(e)}")
        return text


def clean_markdown_tables(text: str) -> str:
    """Clean up malformed markdown tables by normalizing pipe placement"""
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Check if this is a table row (contains pipes)
        if '|' in line:
            # Split by pipes and clean each cell
            parts = line.split('|')
            
            # Remove empty strings from start/end if line starts/ends with pipe
            if parts and parts[0].strip() == '':
                parts = parts[1:]
            if parts and parts[-1].strip() == '':
                parts = parts[:-1]
            
            # Clean each cell (trim whitespace)
            cells = [cell.strip() for cell in parts]
            
            # Check if this is a separator row
            is_separator = all(re.match(r'^[-:\s]+$', cell) for cell in cells if cell)
            
            if is_separator:
                # Rebuild separator row with consistent dashes
                cleaned_cells = ['---' if cell else '---' for cell in cells]
                cleaned_line = '| ' + ' | '.join(cleaned_cells) + ' |'
            else:
                # Regular data row - rebuild with proper spacing
                cleaned_line = '| ' + ' | '.join(cells) + ' |'
            
            cleaned_lines.append(cleaned_line)
        else:
            # Not a table row, keep as is
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)
