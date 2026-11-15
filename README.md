# ContentAddress

[![CI](https://github.com/kapildhinwa2010-dev/ContentAddress/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/ContentAddress/actions/workflows/ci.yml)
[![CI](https://github.com/kapildhinwa2010-dev/ContentAddress/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/ContentAddress/actions/workflows/codeql.yml)

Spiral-addressed memory with XOR parity protection.

**Part of the [Kapildhinwa2010-dev Toolkit](https://github.com/kapildhinwa2010-dev/Kapildhinwa2010-dev).**

## What it does

HelixMemory stores byte records at deterministic string keys, laid out
along a clockwise spiral walk over a square arena. Row XOR parity
detects byte corruption (verify()); corrupt_parity() demonstrates the
one corruption case that repair() can actually fix.

## Install

```bash
pip install -r requirements.txt
```

## Quick start

```python
from contentaddress import HelixMemory

mem = HelixMemory(size=8, record_size=2)
mem.write("a", b"\x10\x20")
assert mem.verify()
```

## API

- write(key, record) / read(key) - spiral-cell storage
- verify() - row XOR parity check
- corrupt_parity(key) - flip the stored parity byte (repairable case)
- repair() - recompute parity from cell data

## Honest results and limitations

- XOR parity DETECTS a flipped byte but cannot locate or repair it:
  a corrupted record byte stays corrupted after repair(); only a
  flipped parity byte is repairable. For real error correction see
  ECC-Memory (Reed-Solomon).
- The arena is a fixed square; no growth or eviction.
- Keys are strings hashed to spiral slots - collisions overwrite.

## License

MIT - see [LICENSE](LICENSE).
