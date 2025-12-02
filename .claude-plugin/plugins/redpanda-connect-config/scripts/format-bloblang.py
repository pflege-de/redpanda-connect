#!/usr/bin/env python3
"""
Format ALL bloblang functions or methods metadata from jsonschema output.
Outputs a tagged format for easy LLM parsing and semantic search.

Usage: rpk connect list --format jsonschema <category> | ./format-bloblang.py
Examples:
    rpk connect list --format jsonschema bloblang-functions | ./format-bloblang.py
    rpk connect list --format jsonschema bloblang-methods | ./format-bloblang.py

Output format:
    <bloblang-functions>
    <uuid_v4>
    Name: uuid_v4
    Category: General
    Description: Generates a new RFC-4122 UUID
    Params: none
    Example: root.id = uuid_v4()
    </uuid_v4>
    ...
    </bloblang-functions>
"""

import sys
import json
from typing import Dict, Any, List


def format_item(item: Dict[str, Any], category_type: str) -> str:
    """Format a single function or method as a tagged section."""
    name = item['name']
    lines = [f"<{name}>"]

    # Category (functions only)
    if "category" in item and item["category"]:
        lines.append(f"Category: {item['category']}")

    # Description (only if meaningful)
    desc = item.get('description', '')
    if desc and desc != 'No description available':
        # Truncate very long descriptions
        if len(desc) > 200:
            desc = desc[:197] + "..."
        lines.append(f"Description: {desc}")

    # Params (only if present)
    params = item.get("params", {}).get("named", [])
    if params:
        param_strs = [f"{p['name']}:{p['type']}" for p in params]
        lines.append(f"Params: {', '.join(param_strs)}")

    # Example (only if present)
    examples = item.get("examples", [])
    if examples:
        example = examples[0]
        if isinstance(example, dict):
            mapping = example.get("mapping", "")
        else:
            mapping = example
        if mapping:  # Only add if not empty
            lines.append(f"Example: {mapping}")

    # Tags (methods only, only if present)
    if "categories" in item:
        categories = item.get("categories", [])
        if categories:
            cat_names = [c.get("Category", str(c)) for c in categories]
            lines.append(f"Tags: {', '.join(cat_names)}")

    lines.append(f"</{name}>")
    return "\n".join(lines)


def main():
    # Read JSON from stdin
    schema = json.load(sys.stdin)

    # Find the category key (bloblang-functions or bloblang-methods)
    category_type = None
    items = None
    for key in ["bloblang-functions", "bloblang-methods"]:
        if key in schema:
            category_type = key
            items = schema[key]
            break

    if not items:
        print("Error: No bloblang items found in schema", file=sys.stderr)
        sys.exit(1)

    # Output opening tag
    print(f"<{category_type}>")

    # Format each item
    formatted_items = []
    for item in items:
        formatted_items.append(format_item(item, category_type))

    # Output all items separated by blank line
    print("\n\n".join(formatted_items))

    # Output closing tag
    print(f"</{category_type}>")


if __name__ == "__main__":
    main()
