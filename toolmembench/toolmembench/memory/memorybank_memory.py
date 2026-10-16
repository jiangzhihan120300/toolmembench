from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9_@.:-]+", (text or "").lower()))


class MemoryBankStyleBackend:
    """Dependency-light MemoryBank-style backend for ToolMemBench.

    It models memory strength, recall reinforcement, and forgetting decay while
    preserving ToolMemBench's add/search contract.
    """

    def __init__(
        self,
        *,
        store_dir: str,
        collection_name: str = "toolmembench_memorybank",
        user_id: str = "toolmembench",
        decay_tau: float = 8.0,
    ):
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        safe_collection = re.sub(r"[^a-zA-Z0-9_.-]+", "_", collection_name)
        safe_user = re.sub(r"[^a-zA-Z0-9_.-]+", "_", user_id)
        self.path = self.store_dir / f"{safe_collection}_{safe_user}.json"
        self.user_id = user_id
        self.decay_tau = decay_tau
        self.step = 0
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _load(self) -> List[Dict[str, Any]]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, rows: List[Dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None, *, infer: bool = False):
        self.step += 1
        rows = self._load()
        memory_id = f"mb_{len(rows)+1:04d}"
        item = {
            "id": memory_id,
            "memory_id": memory_id,
            "memory": content,
            "content": content,
            "metadata": metadata or {},
            "created_step": self.step,
            "last_recall_step": self.step,
            "memory_strength": 1.0,
            "source": (metadata or {}).get("memory_role", "unknown"),
        }
        rows.append(item)
        self._save(rows)
        return item

    def search(self, query: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None):
        self.step += 1
        q = _tokens(query)
        rows = self._load()
        scored = []

        for idx, item in enumerate(rows):
            metadata = item.get("metadata") or {}
            if filters and any(metadata.get(k) != v for k, v in filters.items()):
                continue

            content = item.get("content") or item.get("memory") or ""
            overlap = len(q & _tokens(content))
            if overlap <= 0:
                continue

            strength = float(item.get("memory_strength", 1.0))
            age = max(0, self.step - int(item.get("last_recall_step", self.step)))
            retention = math.exp(-age / max(self.decay_tau * strength, 1e-6))
            score = overlap * (1.0 + math.log1p(strength)) * retention
            scored.append((score, idx, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        selected = scored[:top_k]

        for _, idx, _ in selected:
            rows[idx]["memory_strength"] = float(rows[idx].get("memory_strength", 1.0)) + 1.0
            rows[idx]["last_recall_step"] = self.step
        self._save(rows)

        out = []
        for score, _, item in selected:
            copied = dict(item)
            copied["score"] = score
            copied["memory"] = item.get("memory") or item.get("content") or ""
            copied["content"] = item.get("content") or item.get("memory") or ""
            copied["metadata"] = item.get("metadata") or {}
            out.append(copied)
        return out

    def get_all(self, filters: Optional[Dict[str, Any]] = None):
        rows = self._load()
        if not filters:
            return rows
        return [r for r in rows if all((r.get("metadata") or {}).get(k) == v for k, v in filters.items())]

    def reset_user(self):
        self._save([])

    def close(self):
        return None
