# ContentAddress

ContentAddress is a small Python module that stores byte records in memory under their SHA-256 digests. It also assigns each distinct record a coordinate in a fixed square grid, following a clockwise spiral order.

This is an early, minimal implementation rather than a persistent or production storage system. The whole store is held in process memory and is lost when the process exits.

## Features

- Compute a SHA-256 hexadecimal digest for each byte record and use it as the record key.
- Return the existing digest for repeated identical content, without allocating another slot.
- Retrieve records and check whether a digest is present or whether a stored record still hashes to its digest.
- Assign new records successive coordinates from a center-out spiral over a square grid.
- Report occupied-capacity fraction and raise `MemoryError` when all grid slots are used.

## Requirements and installation

The project metadata requires Python 3.9 or newer and declares `numpy>=1.24` as a dependency. From a checkout, install the project with:

```bash
python -m pip install .
```

The source file can also be imported directly when the repository root is on Python's import path.

## Quick example

```python
from contentaddress import ContentStore

store = ContentStore(size=8)  # 8 × 8 slots
record = b"hello"
digest = store.put(record)

assert store.get(digest) == record
assert store.has(digest)
assert store.verify(digest)
print(digest, store.slot_of(digest), store.usage())
```

`put()` accepts bytes-like input and returns a lowercase SHA-256 hex digest. `get(digest)` raises `KeyError` when the digest is not stored. `has(digest)` returns whether the string key exists, while `verify(digest)` returns `False` for a missing record or a record whose contents no longer match its digest. `slot_of(digest)` returns the assigned `(x, y)` coordinate, or `None` when no slot is recorded. `usage()` returns the fraction of grid slots occupied, and `len(store)` returns the number of distinct records.

The grid dimensions are controlled by `size`; the default is 8, for a capacity of 64 distinct records. `spiral_coordinates(size)` exposes the coordinate sequence and rejects sizes below 1.

## Tests and CI

On the cloned repository commit `bcfaba7d82d974c600b3f7354579a1f912a52d38`, the test suite was run locally with:

```bash
python -m pytest -q
```

Result: **16 passed**. The repository also defines a GitHub Actions workflow to run tests and compile/smoke checks on Python 3.10, 3.11, and 3.12. The hosted workflow's run status was not checked as part of this README review.

## Limitations

- Records and indexes exist only in memory; there is no persistence or recovery after process exit.
- Storage has a fixed `size × size` slot limit. The store does not grow, evict entries, or provide deletion or garbage collection.
- SHA-256 is computed in Python for each `put()`. No throughput or scale benchmarks are provided.
- `verify()` checks that in-memory bytes match their digest; it does not provide authentication, error correction, or repair of corrupted data.
- The public `records` mapping is mutable, so callers can alter stored bytes and cause verification to fail.
- No concurrency guarantees or durable storage backend are implemented.

## License

The repository includes an MIT License. See [LICENSE](LICENSE) for the full text and copyright notice (Copyright © 2026 Kapildhinwa2010-dev).
