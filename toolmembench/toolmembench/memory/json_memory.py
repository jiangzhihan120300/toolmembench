import json
import re
from pathlib import Path

def _tokens(text):
    return set(re.findall(r"[a-zA-Z0-9_@.:-]+", text.lower()))

class JsonMemory:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def all(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def add(self, content, source="unknown", metadata=None):
        data = self.all()
        item = {
            "memory_id": f"m{len(data)+1:04d}",
            "content": content,
            "source": source,
            "metadata": metadata or {},
        }
        data.append(item)
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return item

    def search(self, query, top_k=5):
        q = _tokens(query)
        scored = []
        for item in self.all():
            score = len(q & _tokens(item["content"]))
            if score > 0:
                scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_k]]
