import hashlib

import pytest

from contentaddress import ContentStore, spiral_coordinates


def test_spiral_starts_at_center():
    size = 5
    coords = spiral_coordinates(size)
    assert coords[0] == (2, 2)


def test_spiral_covers_all_cells():
    size = 4
    coords = spiral_coordinates(size)
    assert len(coords) == size * size
    assert len(set(coords)) == size * size


def test_spiral_all_in_bounds():
    size = 6
    for x, y in spiral_coordinates(size):
        assert 0 <= x < size and 0 <= y < size


def test_spiral_rejects_zero():
    with pytest.raises(ValueError):
        spiral_coordinates(0)


def test_spiral_size_one():
    assert spiral_coordinates(1) == [(0, 0)]


# --- content addressing (ContentAddress-specific) ---


def test_put_returns_sha256_digest():
    store = ContentStore(size=4)
    digest = store.put(b"hello")
    assert digest == hashlib.sha256(b"hello").hexdigest()


def test_put_get_roundtrip():
    store = ContentStore(size=4)
    digest = store.put(b"\x01\x02\x03")
    assert store.get(digest) == b"\x01\x02\x03"


def test_dedup_identical_content():
    store = ContentStore(size=4)
    d1 = store.put(b"same")
    d2 = store.put(b"same")
    assert d1 == d2
    assert len(store) == 1
    assert store.usage() == pytest.approx(1 / 16)


def test_distinct_content_distinct_digests():
    store = ContentStore(size=4)
    d1 = store.put(b"a")
    d2 = store.put(b"b")
    assert d1 != d2
    assert len(store) == 2


def test_get_missing_raises_keyerror():
    store = ContentStore(size=4)
    with pytest.raises(KeyError):
        store.get("0" * 64)


def test_get_rejects_non_string():
    store = ContentStore(size=4)
    with pytest.raises(TypeError):
        store.get(123)


def test_verify_true_and_false_after_tamper():
    store = ContentStore(size=4)
    digest = store.put(b"payload")
    assert store.verify(digest) is True
    store.records[digest] = b"tampered"
    assert store.verify(digest) is False


def test_has():
    store = ContentStore(size=4)
    digest = store.put(b"x")
    assert store.has(digest) is True
    assert store.has("f" * 64) is False


def test_slot_assignment_in_spiral_order():
    store = ContentStore(size=4)
    coords = spiral_coordinates(4)
    d1 = store.put(b"first")
    d2 = store.put(b"second")
    assert store.slot_of(d1) == coords[0]
    assert store.slot_of(d2) == coords[1]


def test_store_full_raises():
    store = ContentStore(size=2)
    for i in range(4):
        store.put(bytes([i]))
    with pytest.raises(MemoryError):
        store.put(b"overflow")


def test_constructor_rejects_zero():
    with pytest.raises(ValueError):
        ContentStore(size=0)