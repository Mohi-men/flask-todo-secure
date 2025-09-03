import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ✅ Load local embedding model once at startup
# all-MiniLM-L6-v2 → 384-dimensional embeddings (small & fast)
# you can switch to "multi-qa-mpnet-base-dot-v1" (768-dim, more accurate) if you want
model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(dimension)  # L2 similarity search
task_map = {}
next_id = 0


def embed_text(text: str):
    """Generate embeddings using SentenceTransformers (local)."""
    vec = model.encode(text)
    return np.array(vec, dtype=np.float32)


def build_index(user_tasks):
    """Rebuild FAISS index for a user's tasks."""
    global index, task_map, next_id
    index = faiss.IndexFlatL2(dimension)
    task_map = {}
    next_id = 0

    for t in user_tasks:
        # Build text with metadata
        text = f"{t.content} [Priority: {t.priority}]"
        if t.deadline:
            text += f" (Due {t.deadline.strftime('%Y-%m-%d')})"
        text += " [Completed]" if t.completed else " [Incomplete]"

        # Embed + add to FAISS
        vec = embed_text(text)
        index.add(np.array([vec]))
        task_map[next_id] = text
        next_id += 1


def query_index(query: str, top_k=5):
    """Search FAISS index with a query embedding."""
    if index.ntotal == 0:
        return []
    vec = embed_text(query)
    D, I = index.search(np.array([vec]), top_k)
    return [task_map[i] for i in I[0] if i in task_map]