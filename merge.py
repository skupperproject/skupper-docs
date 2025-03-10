import os
import re
import argparse

DEFAULT_INPUT = "input/index.md"
DEFAULT_OUTPUT = "output/merged.md"

# Regex patterns for detecting links
INLINE_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
DEFINITION_LINK_PATTERN = re.compile(r"^\[([^\]]+)\]:\s*(.*)$", re.MULTILINE)

def extract_md_links(index_file):
    """Extracts markdown file paths from an index.md file, correctly resolving relative links."""
    md_links = []
    base_dir = os.path.dirname(index_file)  # Get directory of index.md
    
    with open(index_file, "r", encoding="utf-8") as f:
        content = f.readlines()
    
    for line in content:
        match = INLINE_LINK_PATTERN.search(line)
        if match:
            link_path = match.group(2).strip()  # Extract link

            # Convert relative paths like ./kube-cli/index.html → kube-cli/index.md
            if link_path.startswith("./"):
                link_path = link_path[2:]  # Remove leading "./"

            md_path = link_path.replace(".html", ".md")  # Convert .html to .md
            full_md_path = os.path.join(base_dir, md_path)  # Resolve full path
            
            if os.path.exists(full_md_path):
                md_links.append(md_path)

    return md_links

def generate_unique_anchor(md_file):
    """Creates a unique anchor using the file's relative path and filename."""
    relative_path = os.path.splitext(md_file)[0]  # Remove .md extension
    anchor = relative_path.replace("/", "-").replace("\\", "-").lower()
    return f"#{anchor}"

def fix_internal_links(content, base_dir, md_file):
    """Fixes internal links so they work within a single merged Markdown file."""
    file_dir = os.path.dirname(md_file)  # Get directory of the file containing links

    def resolve_link(link):
        """Converts relative .html links to .md and then to unique anchors."""
        if link.startswith("http") or link.startswith("#"):
            return link  # Keep absolute links and anchors

        if link.startswith("./"):
            link = link[2:]  # Remove leading "./"

        md_link = link.replace(".html", ".md")
        full_path = os.path.join(base_dir, file_dir, md_link)  # Resolve relative to the file's dir

        if os.path.exists(full_path):
            return generate_unique_anchor(os.path.relpath(full_path, base_dir))  # Use full relative path

        return link  # Return unchanged if file not found

    # Fix inline links: `[Text](./page.html)`
    content = INLINE_LINK_PATTERN.sub(lambda m: f"[{m.group(1)}]({resolve_link(m.group(2))})", content)

    # Fix reference-style links: `[ref]: ./page.html`
    content = DEFINITION_LINK_PATTERN.sub(lambda m: f"[{m.group(1)}]: {resolve_link(m.group(2))}", content)

    return content

def merge_markdown(index_file, output_file):
    """Merges markdown files into a single file while fixing internal links."""
    base_dir = os.path.dirname(index_file)
    md_links = extract_md_links(index_file)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    merged_content = []

    for md_file in md_links:
        full_path = os.path.join(base_dir, md_file)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            content = fix_internal_links(content, base_dir, md_file)
            anchor = generate_unique_anchor(os.path.relpath(full_path, base_dir))

            # Insert an HTML anchor so internal linking works
            merged_content.append(f"<a id='{anchor[1:]}'></a>\n" + content.strip())

    with open(output_file, "w", encoding="utf-8") as out_f:
        out_f.write("\n\n".join(merged_content) + "\n")

    print(f"Merged markdown saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge nested markdown files into a single file while fixing internal links.")
    parser.add_argument("index_file", nargs="?", default=DEFAULT_INPUT, help="Path to the index.md file (default: input/index.md)")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="Output file (default: output/merged.md)")
    
    args = parser.parse_args()
    merge_markdown(args.index_file, args.output)
