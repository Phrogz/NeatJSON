"""
NeatJSON - Pretty-print JSON with more power than json.dumps provides.

This module provides a single function, `neat_json`, which generates
formatted JSON strings with extensive customization options.

Example:
    >>> from neatjson import neat_json
    >>> print(neat_json({"a": 1, "b": [2, 3]}, sort=True, wrap=40))
    {
      "a":1,
      "b":[2,3]
    }
"""

from __future__ import annotations

import dataclasses
import inspect
import json
import math
import re
from collections.abc import Callable, Iterable
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from typing import Any

__version__ = "0.10.7"
__all__ = ["neat_json", "__version__"]


def neat_json(
    value: Any,
    *,
    wrap: int | bool = 80,
    indent: str = "  ",
    indent_last: bool = False,
    short: bool = False,
    sort: bool | Callable[..., Any] = False,
    sorted: bool | Callable[..., Any] | None = None,  # noqa: A002 - alias for sort
    aligned: bool = False,
    decimals: int | None = None,
    trim_trailing_zeros: bool = False,
    force_floats: bool = False,
    force_floats_in: list[str] | None = None,
    padding: int = 0,
    array_padding: int | None = None,
    object_padding: int | None = None,
    around_comma: int = 0,
    before_comma: int | None = None,
    after_comma: int | None = None,
    around_colon: int = 0,
    before_colon: int | None = None,
    after_colon: int | None = None,
    around_colon_1: int | None = None,
    before_colon_1: int | None = None,
    after_colon_1: int | None = None,
    around_colon_n: int | None = None,
    before_colon_n: int | None = None,
    after_colon_n: int | None = None,
) -> str:
    """
    Generate a formatted JSON string representation of a value.

    Args:
        value: The value to serialize to JSON.
        wrap: Maximum line width before wrapping. Use False to never wrap,
              True to always wrap. Default: 80
        indent: Whitespace used to indent each level when wrapping.
                Default: "  " (two spaces)
        indent_last: Indent the closing bracket/brace for arrays and objects.
                     Default: False
        short: Put opening brackets on the same line as the first value,
               closing brackets on the same line as the last. Default: False
        sort: Sort object keys alphabetically (True), or provide a callable
              for custom sorting. The callable receives 1-3 arguments:
              (key), (key, value), or (key, value, obj). Default: False
        sorted: Alias for sort.
        aligned: When wrapping objects, align the colons. Default: False
        decimals: Decimal precision for floats. None keeps values precise.
                  Default: None
        trim_trailing_zeros: Remove trailing zeros from decimals output.
                             Default: False
        force_floats: Force all integers to be written as floats (e.g. 12 → 12.0).
                      Default: False
        force_floats_in: List of object key names under which integers are
                         written as floats. Default: None
        padding: Shorthand for both array_padding and object_padding.
                 Default: 0
        array_padding: Spaces inside brackets for arrays. Default: 0
        object_padding: Spaces inside braces for objects. Default: 0
        around_comma: Shorthand for before_comma and after_comma. Default: 0
        before_comma: Spaces before commas. Default: 0
        after_comma: Spaces after commas. Default: 0
        around_colon: Shorthand for before_colon and after_colon. Default: 0
        before_colon: Shorthand for before_colon_1 and before_colon_n.
                      Default: 0
        after_colon: Shorthand for after_colon_1 and after_colon_n. Default: 0
        around_colon_1: Shorthand for before_colon_1 and after_colon_1.
                        Default: 0
        before_colon_1: Spaces before colons for single-line objects.
                        Default: 0
        after_colon_1: Spaces after colons for single-line objects. Default: 0
        around_colon_n: Shorthand for before_colon_n and after_colon_n.
                        Default: 0
        before_colon_n: Spaces before colons for multi-line objects.
                        Default: 0
        after_colon_n: Spaces after colons for multi-line objects. Default: 0

    Returns:
        A formatted JSON string.

    Examples:
        >>> neat_json({"a": 1, "b": 2})
        '{"a":1,"b":2}'

        >>> neat_json([1, 2, 3], array_padding=1)
        '[ 1,2,3 ]'

        >>> neat_json({"a": 1}, wrap=True)
        '{\\n  "a":1\\n}'
    """
    # Handle wrap special values
    wrap_width: int | None
    if wrap is True:
        wrap_width = -1  # Always wrap
    elif wrap is False:
        wrap_width = None  # Never wrap
    else:
        wrap_width = wrap

    # Resolve option cascades
    _array_padding = array_padding if array_padding is not None else padding
    _object_padding = object_padding if object_padding is not None else padding
    _before_comma = before_comma if before_comma is not None else around_comma
    _after_comma = after_comma if after_comma is not None else around_comma
    _before_colon = before_colon if before_colon is not None else around_colon
    _after_colon = after_colon if after_colon is not None else around_colon
    _before_colon_1 = (
        before_colon_1
        if before_colon_1 is not None
        else (around_colon_1 if around_colon_1 is not None else _before_colon)
    )
    _after_colon_1 = (
        after_colon_1
        if after_colon_1 is not None
        else (around_colon_1 if around_colon_1 is not None else _after_colon)
    )
    _before_colon_n = (
        before_colon_n
        if before_colon_n is not None
        else (around_colon_n if around_colon_n is not None else _before_colon)
    )
    _after_colon_n = (
        after_colon_n
        if after_colon_n is not None
        else (around_colon_n if around_colon_n is not None else _after_colon)
    )

    # Handle sort/sorted alias
    sort_opt = sorted if sorted is not None else sort

    # Normalize force_floats_in to empty list if None
    _force_floats_in: list[str] = force_floats_in if force_floats_in is not None else []

    # Pre-compute formatting strings
    apad = " " * _array_padding
    opad = " " * _object_padding
    comma = f"{' ' * _before_comma},{' ' * _after_comma}"
    colon1 = f"{' ' * _before_colon_1}:{' ' * _after_colon_1}"
    colonn = f"{' ' * _before_colon_n}:{' ' * _after_colon_n}"

    # Memoization cache keyed by (id(obj), indent, floats_forced)
    # Only used for arrays and objects where recursion can repeat
    memo: dict[tuple[int, str, bool], str] = {}

    def build(obj: Any, ind: str, floats_forced: bool) -> str:
        """Recursively build the JSON string for an object."""
        # Only memoize complex objects (arrays/dicts) where caching helps
        # Simple values like int/float can have id() collisions with temporary objects
        if isinstance(obj, (list, tuple, set, frozenset, dict)):
            cache_key = (id(obj), ind, floats_forced)
            if cache_key in memo:
                return memo[cache_key]
            result = _build_value(obj, ind, floats_forced)
            memo[cache_key] = result
            return result

        return _build_value(obj, ind, floats_forced)

    def _build_value(obj: Any, ind: str, floats_forced: bool) -> str:
        """Build the JSON string for a single value."""
        match obj:
            case str():
                return f"{ind}{json.dumps(obj)}"

            case bool():
                # Must come before int check since bool is subclass of int
                return f"{ind}{str(obj).lower()}"

            case int():
                if floats_forced:
                    return build(float(obj), ind, floats_forced)
                return f"{ind}{obj}"

            case float():
                # Handle infinity and NaN
                if math.isinf(obj):
                    return f"{ind}{'-9e9999' if obj < 0 else '9e9999'}"
                if math.isnan(obj):
                    return f'{ind}"NaN"'

                # Check if float is equivalent to integer (and not forced)
                if not floats_forced and obj == int(obj) and not re.search(r"e", str(obj), re.IGNORECASE):
                    return build(int(obj), ind, floats_forced)

                if decimals is not None:
                    if trim_trailing_zeros:
                        return f"{ind}{round(obj, decimals)}"
                    else:
                        return f"{ind}{obj:.{decimals}f}"
                else:
                    return f"{ind}{obj}"

            case Decimal() | Fraction():
                # Convert to float for JSON serialization
                float_val = float(obj)
                return build(float_val, ind, floats_forced)

            case None:
                return f"{ind}null"

            case list() | set() | frozenset():
                return _build_array(list(obj), ind, floats_forced)

            case tuple():
                # Check for namedtuple (has _asdict and _fields)
                if hasattr(obj, "_asdict") and hasattr(obj, "_fields"):
                    return _build_value(getattr(obj, "_asdict")(), ind, floats_forced)
                return _build_array(list(obj), ind, floats_forced)

            case dict():
                return _build_object(obj, ind, floats_forced)

            case _:
                # Check for __json__ method first
                if hasattr(obj, "__json__"):
                    json_value = obj.__json__()
                    # Don't memoize __json__ result - build it directly
                    return _build_value(json_value, ind, floats_forced)

                # Enum: use the value
                if isinstance(obj, Enum):
                    return _build_value(obj.value, ind, floats_forced)

                # Dataclass: convert to dict
                if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
                    return _build_value(dataclasses.asdict(obj), ind, floats_forced)

                # Other iterables (range, deque, generators, etc.): convert to list
                if isinstance(obj, Iterable):
                    return _build_array(list(obj), ind, floats_forced)

                # Fall back to json.dumps for other types
                return f"{ind}{json.dumps(obj)}"

    def _build_array(arr: list[Any], ind: str, floats_forced: bool) -> str:
        """Build the JSON string for an array."""
        if not arr:
            return f"{ind}[]"

        pieces = [build(v, "", floats_forced) for v in arr]
        one_line = f"{ind}[{apad}{comma.join(pieces)}{apad}]"

        if wrap_width is None or len(one_line) <= wrap_width:
            return one_line

        if short:
            indent2 = f"{ind} {apad}"
            pieces = [build(v, indent2, floats_forced) for v in arr]
            pieces[0] = pieces[0].replace(indent2, f"{ind}[{apad}", 1)
            pieces[-1] = f"{pieces[-1]}{apad}]"
            return ",\n".join(pieces)
        else:
            indent2 = f"{ind}{indent}"
            inner = ",\n".join(build(v, indent2, floats_forced) for v in arr)
            close_ind = indent2 if indent_last else ind
            return f"{ind}[\n{inner}\n{close_ind}]"

    def _build_object(obj: dict[Any, Any], ind: str, floats_forced: bool) -> str:
        """Build the JSON string for an object."""
        if not obj:
            return f"{ind}{{}}"

        # Convert to list of items for potential sorting
        items: list[tuple[Any, Any]] = list(obj.items())

        # Handle sorting
        if sort_opt:
            if sort_opt is True:
                items = builtins_sorted(items, key=lambda kv: str(kv[0]))
            elif callable(sort_opt):
                # Determine arity of sort function
                try:
                    sig = inspect.signature(sort_opt)
                    # Count params that could accept positional arguments
                    max_arity = len(
                        [
                            p
                            for p in sig.parameters.values()
                            if p.kind
                            in (
                                inspect.Parameter.POSITIONAL_ONLY,
                                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                            )
                        ]
                    )
                except (ValueError, TypeError):
                    max_arity = 1

                # sort_opt is confirmed callable at this point
                sort_fn = sort_opt  # type: Callable[..., Any]
                if max_arity >= 3:
                    items = builtins_sorted(
                        items, key=lambda kv: sort_fn(kv[0], kv[1], obj)
                    )
                elif max_arity >= 2:
                    items = builtins_sorted(items, key=lambda kv: sort_fn(kv[0], kv[1]))
                else:
                    items = builtins_sorted(items, key=lambda kv: sort_fn(kv[0]))

        # Get string keys for force_floats_in lookup
        keys = [str(k) for k, _ in items]

        # Build key-value strings for single line attempt
        keyvals_1 = [
            (json.dumps(str(k)), build(v, "", force_floats or keys[i] in _force_floats_in))
            for i, (k, v) in enumerate(items)
        ]
        keyvals_str = comma.join(f"{k}{colon1}{v}" for k, v in keyvals_1)
        one_line = f"{ind}{{{opad}{keyvals_str}{opad}}}"

        if wrap_width is None or len(one_line) <= wrap_width:
            return one_line

        # Multi-line formatting
        if short:
            keyvals = [[f"{ind} {opad}{json.dumps(str(k))}", v, i] for i, (k, v) in enumerate(items)]
            keyvals[0][0] = keyvals[0][0].replace(f"{ind} ", f"{ind}{{", 1)

            if aligned:
                longest = max(len(kv[0]) for kv in keyvals)
                keyvals = [[kv[0].ljust(longest), kv[1], kv[2]] for kv in keyvals]

            result_lines: list[str] = []
            for k_str, v, idx in keyvals:
                key_floats_forced = force_floats or keys[idx] in _force_floats_in
                indent2 = " " * len(f"{k_str}{colonn}")
                one_line_kv = f"{k_str}{colonn}{build(v, '', key_floats_forced)}"
                if (
                    wrap_width is not None
                    and len(one_line_kv) > wrap_width
                    and isinstance(v, (list, tuple, set, frozenset, dict))
                ):
                    result_lines.append(f"{k_str}{colonn}{build(v, indent2, key_floats_forced).lstrip()}")
                else:
                    result_lines.append(one_line_kv)

            return f"{',\n'.join(result_lines)}{opad}}}"
        else:
            keyvals = [[f"{ind}{indent}{json.dumps(str(k))}", v, i] for i, (k, v) in enumerate(items)]

            if aligned:
                longest = max(len(kv[0]) for kv in keyvals)
                keyvals = [[kv[0].ljust(longest), kv[1], kv[2]] for kv in keyvals]

            indent2 = f"{ind}{indent}"
            result_lines = []
            for k_str, v, idx in keyvals:
                key_floats_forced = force_floats or keys[idx] in _force_floats_in
                one_line_kv = f"{k_str}{colonn}{build(v, '', key_floats_forced)}"
                if (
                    wrap_width is not None
                    and len(one_line_kv) > wrap_width
                    and isinstance(v, (list, tuple, set, frozenset, dict))
                ):
                    result_lines.append(f"{k_str}{colonn}{build(v, indent2, key_floats_forced).lstrip()}")
                else:
                    result_lines.append(one_line_kv)

            close_ind = indent2 if indent_last else ind
            return f"{ind}{{\n{',\n'.join(result_lines)}\n{close_ind}}}"

    # Avoid shadowing built-in sorted
    builtins_sorted = __builtins__["sorted"] if isinstance(__builtins__, dict) else getattr(__builtins__, "sorted")  # type: ignore[index]

    return build(value, "", force_floats)
