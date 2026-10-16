from __future__ import annotations


def make_memory_backend(
    backend: str,
    *,
    store_dir: str,
    collection_name: str,
    user_id: str,
):
    backend = (backend or "mem0").lower()

    if backend == "mem0":
        from toolmembench.memory.mem0_memory import Mem0MemoryBackend
        return Mem0MemoryBackend(
            store_dir=store_dir,
            collection_name=collection_name,
            user_id=user_id,
        )

    if backend in {"memorybank", "memorybank_style"}:
        from toolmembench.memory.memorybank_memory import MemoryBankStyleBackend
        return MemoryBankStyleBackend(
            store_dir=store_dir,
            collection_name=collection_name,
            user_id=user_id,
        )

    if backend in {"memoryos", "memoryos_style"}:
        from toolmembench.memory.memoryos_memory import MemoryOSStyleBackend
        return MemoryOSStyleBackend(
            store_dir=store_dir,
            collection_name=collection_name,
            user_id=user_id,
        )

    raise ValueError(f"unknown memory backend: {backend}")
