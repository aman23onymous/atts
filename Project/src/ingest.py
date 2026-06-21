from pathlib import Path


def read_cpp_templates(templates_dir: str) -> list[dict]:
    """
    Reads all .cpp files from the designated directory and extracts their contents.
    Returns a list of dictionaries containing raw text and file metadata.
    """
    documents = []
    templates_path = Path(templates_dir)

    if not templates_path.exists():
        print(f"Error: Directory '{templates_dir}' does not exist.")
        return documents

    for file_path in templates_path.glob("*.cpp"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            documents.append({
                "content": content,
                "metadata": {
                    "filename": file_path.name,
                    "path": str(file_path),
                    "algorithm_name": file_path.stem.replace("_", " ").title()
                }
            })
        except Exception as e:
            print(f"Failed to read {file_path.name}: {e}")

    return documents


def chunk_code(documents: list[dict], max_chunk_size: int = 1000, overlap: int = 100) -> list[dict]:
    """
    Splits long code documents into smaller chunks while preserving metadata.
    Uses line-based chunking so code stays readable and does not cut mid-statement.
    """
    if max_chunk_size <= 0:
        raise ValueError("max_chunk_size must be greater than 0")

    chunks = []

    for doc in documents:
        content = doc["content"]
        metadata = doc["metadata"]

        if not content.strip():
            continue

        if len(content) <= max_chunk_size:
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_id"] = 0
            chunks.append({
                "content": content,
                "metadata": chunk_metadata
            })
            continue

        lines = content.splitlines(keepends=True)
        current_lines = []
        current_len = 0
        chunk_id = 0

        def flush_current():
            nonlocal current_lines, current_len, chunk_id
            if not current_lines:
                return
            chunk_text = "".join(current_lines)
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_id"] = chunk_id
            chunks.append({
                "content": chunk_text,
                "metadata": chunk_metadata
            })
            chunk_id += 1
            current_lines = []
            current_len = 0

        for line in lines:
            line_len = len(line)

            if current_lines and current_len + line_len > max_chunk_size:
                flush_current()

            if line_len > max_chunk_size:
                if current_lines:
                    flush_current()
                start = 0
                while start < line_len:
                    end = min(line_len, start + max_chunk_size)
                    chunk_metadata = metadata.copy()
                    chunk_metadata["chunk_id"] = chunk_id
                    chunks.append({
                        "content": line[start:end],
                        "metadata": chunk_metadata
                    })
                    chunk_id += 1
                    start = end
                continue

            current_lines.append(line)
            current_len += line_len

        flush_current()

    return chunks


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    TEMPLATES_DIR = PROJECT_ROOT / "templates"

    print("--- Starting Phase 2: Ingestion ---")
    raw_docs = read_cpp_templates(str(TEMPLATES_DIR))
    print(f"Successfully read {len(raw_docs)} C++ template files.")

    processed_chunks = chunk_code(raw_docs, max_chunk_size=1200, overlap=150)
    print(f"Generated {len(processed_chunks)} total chunks for the vector database.")

    if processed_chunks:
        print("\n--- Sample Chunk Metadata ---")
        print(processed_chunks[0]["metadata"])
