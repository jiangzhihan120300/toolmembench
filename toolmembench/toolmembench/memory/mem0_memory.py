import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from mem0 import Memory

class Mem0MemoryBackend:
    def __init__(
        self,
        *,
        store_dir: str,
        collection_name: str = "toolmembench_mem0",
        user_id: str = "toolmembench",
        embedding_model: str = "BAAI/bge-small-en-v1.5",
        embedding_dims: int = 384,
    ):
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.user_id = user_id

        api_key = os.environ.get("TOOLMEMBENCH_API_KEY", "")
        base_url = os.environ.get("TOOLMEMBENCH_BASE_URL", "https://api.deepseek.com")
        model = os.environ.get("TOOLMEMBENCH_MODEL", "deepseek-chat")

        config = {
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "path": str(self.store_dir / "qdrant"),
                    "collection_name": collection_name,
                    "embedding_model_dims": embedding_dims,
                },
            },
            "embedder": {
                "provider": "fastembed",
                "config": {
                    "model": embedding_model,
                },
            },
            "llm": {
                "provider": "deepseek",
                "config": {
                    "api_key": api_key,
                    "model": model,
                    "deepseek_base_url": base_url,
                },
            },
            "history_db_path": str(self.store_dir / "history.db"),
        }
        self.memory = Memory.from_config(config)

    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None, *, infer: bool = False):
        return self.memory.add(
            content,
            user_id=self.user_id,
            metadata=metadata or {},
            infer=infer,
        )

    def search(self, query: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        merged_filters = {"user_id": self.user_id}
        if filters:
            merged_filters.update(filters)

        result = self.memory.search(
            query,
            filters=merged_filters,
            top_k=top_k,
        )
        if isinstance(result, dict):
            return result.get("results", [])
        if isinstance(result, list):
            return result
        return []

    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        merged_filters = {"user_id": self.user_id}
        if filters:
            merged_filters.update(filters)
        result = self.memory.get_all(filters=merged_filters)
        if isinstance(result, dict):
            return result.get("results", [])
        if isinstance(result, list):
            return result
        return []

    def reset_user(self):
        return self.memory.delete_all(user_id=self.user_id)

    def close(self):
        try:
            self.memory.close()
        except Exception:
            pass
