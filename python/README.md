# NeatJSON for Python

Pretty-print your JSON in Python with more power than `json.dumps` provides.

See the [main project README](../README.md) for full documentation.

## Installation

```bash
pip install neatjson
```

## Quick Start

```python
from neatjson import neat_json

data = {"b": 42.005, "a": [42, 17], "longer": True, "str": "yes\nplease"}

# Compact output (default)
print(neat_json(data))
# {"b":42.005,"a":[42,17],"longer":true,"str":"yes\nplease"}

# Sorted keys
print(neat_json(data, sort=True))
# {"a":[42,17],"b":42.005,"longer":true,"str":"yes\nplease"}

# Wrapped with indentation
print(neat_json(data, sort=True, wrap=40))
# {
#   "a":[42,17],
#   "b":42.005,
#   "longer":true,
#   "str":"yes\nplease"
# }
```

## Python-Specific Features

The following Python types are automatically handled:

- **Tuples, sets, and frozensets** are serialized as JSON arrays
- **Other iterables** (`range`, `deque`, generators, etc.) are serialized as arrays
- **namedtuple** instances are serialized as JSON objects (using field names as keys)
- **dataclasses** are serialized as JSON objects
- **Enum** values are serialized using their `.value`
- **Decimal** and **Fraction** are serialized as JSON numbers
- Objects with a `__json__()` method will have that method called for serialization

## Development

```bash
cd python
pip install -e ".[dev]"
pytest
```
