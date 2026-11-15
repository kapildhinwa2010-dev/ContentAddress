# ContentAddress - Content-addressed storage with SHA-256 addressing
# Part of the Kapildhinwa2010-dev Toolkit.

"""Immutable content-addressed store keyed by SHA-256 digests.

Lineage: reserv.dean-part-2 (helix.py). Records are stored ONCE keyed by
their SHA-256 hex digest; identical content is deduplicated automatically
and integrity is verifiable by re-hashing. Spiral coordinates allocate
slots in insertion order.

HONEST LIMITATIONS: the whole store lives in memory (no persistence),
SHA-256 is computed in Python per put (fine for small records, not a
high-throughput store), and there is no garbage collection.
"""

from __future__ import annotations

import hashlib

__all__ = ["spiral_coordinates", "ContentStore"]


def spiral_coordinates(size: int):
    """Clockwise spiral walk of an ``size x size`` grid from the center."""
    if size < 1:
        raise ValueError("size must be >= 1")
    coords = []
    x = y = size // 2
    coords.append((x, y))
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # right, down, left, up
    step = 1
    while len(coords) < size * size:
        for d_index, (dx, dy) in enumerate(directions):
            length = step
            for _ in range(length):
                if len(coords) >= size * size:
                    return coords
                x += dx
                y += dy
                if 0 <= x < size and 0 <= y < size:
                    coords.append((x, y))
            if d_index % 2 == 1:
                step += 1
    return coords


class ContentStore:
    """In-memory content-addressed store: put(record) -> sha256 digest."""

    def __init__(self, size: int = 8) -> None:
        if size < 1:
            raise ValueError("size must be >= 1")
        self.size = int(size)
        self.coords = spiral_coordinates(size)
        self.records: dict = {}   # digest -> bytes
        self.slots: dict = {}     # digest -> spiral (x, y)

    def put(self, record: bytes) -> str:
        """Store ``record`` once; return its SHA-256 hex digest.

        Putting identical content twice is a no-op (dedup) and returns
        the same digest.
        """
        record = bytes(record)
        digest = hashlib.sha256(record).hexdigest()
        if digest not in self.records:
            if len(self.records) >= len(self.coords):
                raise MemoryError("store is full: {} slots".format(len(self.coords)))
            self.slots[digest] = self.coords[len(self.slots)]
            self.records[digest] = record
        return digest

    def get(self, digest: str) -> bytes:
        """Return the record for ``digest``; KeyError if absent."""
        if not isinstance(digest, str):
            raise TypeError("digest must be a hex string")
        if digest not in self.records:
            raise KeyError(digest)
        return self.records[digest]

    def has(self, digest: str) -> bool:
        return isinstance(digest, str) and digest in self.records

    def verify(self, digest: str) -> bool:
        """True when the stored record still hashes to ``digest``."""
        if not self.has(digest):
            return False
        return hashlib.sha256(self.records[digest]).hexdigest() == digest

    def slot_of(self, digest: str):
        """Spiral (x, y) slot assigned to ``digest``, or None."""
        return self.slots.get(digest)

    def usage(self) -> float:
        return len(self.records) / len(self.coords)

    def __len__(self) -> int:
        return len(self.records)