from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9_@.:-]+", (text or "").lower()))


class MemoryOSStyleBackend:
    """Dependency-light MemoryOS-style backend for ToolMemBench.

    It models short/mid/long memory layers and a bounded retrieval queue while
    preserving ToolMemBench's add/search contract.
    """

    def __init__(
        self,
        *,
        store_dir: str,
        collection_name: str = "toolmembench_memoryos",
        user_id: str = "toolmembench",
        short_capacity: int = 2,
        retrieval_queue_capacity: int = 5,
    ):
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        safe_collection = re.sub(r"[^a-zA-Z0-9_.-]+", "_", collection_name)
        safe_user = re.sub(r"[^a-zA-Z0-9_.-]+", "_", user_id)
        self.path = self.store_dir / f"{safe_collection}_{safe_user}.json"
        self.user_id = user_id
        self.short_capacity = short_capacity
        self.retrieval_queue_capacity = retrieval_queue_capacity
        self.step = 0
        if not self.path.exists():
            self._save({"short": [], "mid": [], "long": []})

    def _load(self) -> Dict[str, List[Dict[str, Any]]]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _all_rows(self, data):
        return list(data.get("short", [])) + list(data.get("mid", [])) + list(data.get("long", []))

    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None, *, infer: bool = False):
        self.step += 1
        data = self._load()
        n = sum(len(v) for v in data.values())
        memory_id = f"mos_{n+1:04d}"
        item = {
            "id": memory_id,
            "memory_id": memory_id,
            "memory": content,
            "content": content,
            "metadata": metadata or {},
            "created_step": self.step,
            "last_recall_step": self.step,
            "access_count": 0,
            "tier": "short",
        }
        data.setdefault("short", []).append(item)

        while len(data["short"]) > self.short_capacity:
            moved = data["short"].pop(0)
            moved["tier"] = "mid"
            data.setdefault("mid", []).append(moved)

        kept_mid = []
        for row in data.get("mid", []):
            if int(row.get("access_count", 0)) >= 3:
                row["tier"] = "long"
                data.setdefault("long", []).append(row)
            else:
                kept_mid.append(row)
        data["mid"] = kept_mid

        self._save(data)
        return item

    def search(self, query: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None):
        self.step += 1
        data = self._load()
        q = _tokens(query)
        scored = []
        tier_bonus = {"short": 0.35, "mid": 0.15, "long": 0.05}

        for tier in ("short", "mid", "long"):
            for idx, item in enumerate(data.get(tier, [])):
                metadata = item.get("metadata") or {}
                if filters and any(metadata.get(k) != v for k, v in filters.items()):
                    continue

                content = item.get("content") or item.get("memory") or ""
                overlap = len(q & _tokens(content))
                if overlap <= 0:
                    continue

                access = int(item.get("access_count", 0))
                recency = 1.0 / (1.0 + max(0, self.step - int(item.get("last_recall_step", self.step))))
                score = overlap + tier_bonus.get(tier, 0.0) + 0.1 * access + 0.1 * recency
                scored.append((score, tier, idx, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        selected = scored[: min(top_k, self.retrieval_queue_capacity)]

        for _, tier, idx, _ in selected:
            data[tier][idx]["access_count"] = int(data[tier][idx].get("access_count", 0)) + 1
            data[tier][idx]["last_recall_step"] = self.step
        self._save(data)

        out = []
        for score, tier, _, item in selected:
            copied = dict(item)
            copied["score"] = score
            copied["tier"] = tier
            copied["memory"] = item.get("memory") or item.get("content") or ""
            copied["content"] = item.get("content") or item.get("memory") or ""
            copied["metadata"] = item.get("metadata") or {}
            out.append(copied)
        return out

    def get_all(self, filters: Optional[Dict[str, Any]] = None):
        rows = self._all_rows(self._load())
        if not filters:
            return rows
        return [r for r in rows if all((r.get("metadata") or {}).get(k) == v for k, v in filters.items())]

    def reset_user(self):
        self._save({"short": [], "mid": [], "long": []})

    def close(self):
        return None
