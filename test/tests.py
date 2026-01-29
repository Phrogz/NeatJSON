"""
Test data for NeatJSON Python port.

Each test case is a dict with 'value' and 'tests' keys.
'tests' is a list of dicts with 'json' (expected output) and optional 'opts'.
The 'json' value can be a string or a compiled regex pattern.
"""

from __future__ import annotations

import math
import re
from typing import Any

TESTS: list[dict[str, Any]] = [
    {"value": True, "tests": [{"json": "true"}]},
    {"value": False, "tests": [{"json": "false"}]},
    {"value": None, "tests": [{"json": "null"}]},
    {"value": 5, "tests": [
        {"json": "5"},
        {"json": "5", "opts": {"decimals": 3}},
    ]},
    {"value": 5.0, "tests": [
        {"json": "5"},
        {"json": "5", "opts": {"decimals": 3}},
    ]},
    {"value": 5.0001, "tests": [
        {"json": "5.0001"},
        {"json": "5.000", "opts": {"decimals": 3}},
        {"json": "5.0", "opts": {"decimals": 3, "trim_trailing_zeros": True, "force_floats": True}},
        {"json": "5.000", "opts": {"decimals": 3, "trim_trailing_zeros": False, "force_floats": True}},
    ]},
    {"value": 4.2, "tests": [
        {"json": "4.2"},
        {"json": "4", "opts": {"decimals": 0}},
        {"json": "4.20", "opts": {"decimals": 2}},
    ]},
    {"value": 4.199, "tests": [{"json": "4.20", "opts": {"decimals": 2}}]},
    {"value": 4.204, "tests": [{"json": "4.20", "opts": {"decimals": 2}}]},
    {"value": -1.9, "tests": [{"json": "-2", "opts": {"decimals": 0}}]},
    {"value": -2.4, "tests": [{"json": "-2", "opts": {"decimals": 0}}]},
    {"value": 1e23, "tests": [{"json": re.compile(r"1(?:\.0+)?e\+23", re.IGNORECASE)}]},
    {"value": 1e-9, "tests": [{"json": re.compile(r"1(?:\.0+)?e-0*9", re.IGNORECASE)}]},
    {"value": -2.4, "tests": [{"json": "-2", "opts": {"decimals": 0}}]},

    # String tests
    {"value": "foo", "tests": [{"json": '"foo"'}]},
    {"value": "foo\nbar", "tests": [{"json": '"foo\\nbar"'}]},
    {"value": "foo\tbar", "tests": [{"json": '"foo\\tbar"'}]},
    {"value": "foo\rbar", "tests": [{"json": '"foo\\rbar"'}]},
    {"value": "foo\bbar", "tests": [{"json": '"foo\\bbar"'}]},
    {"value": "foo\fbar", "tests": [{"json": '"foo\\fbar"'}]},
    {"value": "foo${no}bar", "tests": [{"json": '"foo${no}bar"'}]},
    {"value": "foo#{no}bar", "tests": [{"json": '"foo#{no}bar"'}]},
    {"value": "foo\\bar", "tests": [{"json": '"foo\\\\bar"'}]},
    {"value": "foo/bar", "tests": [{"json": '"foo/bar"'}]},

    {"value": [1, 2, 3, 4, [5, 6, 7, [8, 9, 10], 11, 12]], "tests": [
        {"json": "[1,2,3,4,[5,6,7,[8,9,10],11,12]]"},
        {"json": "[\n  1,\n  2,\n  3,\n  4,\n  [5,6,7,[8,9,10],11,12]\n]", "opts": {"wrap": 30}},
        {"json": "[\n  1,\n  2,\n  3,\n  4,\n  [\n    5,\n    6,\n    7,\n    [8,9,10],\n    11,\n    12\n  ]\n]", "opts": {"wrap": 20}},
        {"json": "[\n  1,\n  2,\n  3,\n  4,\n  [\n    5,\n    6,\n    7,\n    [\n      8,\n      9,\n      10\n    ],\n    11,\n    12\n  ]\n]", "opts": {"wrap": True}},
        {"json": "[\n\t1,\n\t2,\n\t3,\n\t4,\n\t[\n\t\t5,\n\t\t6,\n\t\t7,\n\t\t[\n\t\t\t8,\n\t\t\t9,\n\t\t\t10\n\t\t],\n\t\t11,\n\t\t12\n\t]\n]", "opts": {"wrap": True, "indent": "\t"}},
        {"json": "[1,2,3,4,[5,6,7,[8,9,10],11,12]]", "opts": {"array_padding": 0}},
        {"json": "[ 1,2,3,4,[ 5,6,7,[ 8,9,10 ],11,12 ] ]", "opts": {"array_padding": 1}},
        {"json": "[  1,2,3,4,[  5,6,7,[  8,9,10  ],11,12  ]  ]", "opts": {"array_padding": 2}},
        {"json": "[1, 2, 3, 4, [5, 6, 7, [8, 9, 10], 11, 12]]", "opts": {"after_comma": 1}},
        {"json": "[ 1, 2, 3, 4, [ 5, 6, 7, [ 8, 9, 10 ], 11, 12 ] ]", "opts": {"after_comma": 1, "array_padding": 1}},
        {"json": "[1,\n 2,\n 3,\n 4,\n [5,\n  6,\n  7,\n  [8,\n   9,\n   10],\n  11,\n  12]]", "opts": {"short": True, "wrap": True}},
        {"json": "[1,\n 2,\n 3,\n 4,\n [5,\n  6,\n  7,\n  [8,\n   9,\n   10],\n  11,\n  12]]", "opts": {"short": True, "wrap": True, "after_comma": 1}},
        {"json": "[ 1,\n  2,\n  3,\n  4,\n  [ 5,\n    6,\n    7,\n    [ 8,\n      9,\n      10 ],\n    11,\n    12 ] ]", "opts": {"short": True, "wrap": True, "array_padding": 1}},
    ]},

    {"value": [1, 2, 3], "tests": [
        {"json": "[1,2,3]"},
        {"json": "[1 ,2 ,3]", "opts": {"before_comma": 1}},
        {"json": "[1 , 2 , 3]", "opts": {"around_comma": 1}},
    ]},

    {"value": {"b": 1, "a": 2}, "tests": [
        {"json": '{"b":1,"a":2}'},
        {"json": '{"a":2,"b":1}', "opts": {"sorted": True}},
        {"json": '{"a":2,"b":1}', "opts": {"sort": True}},
        {"json": '{"a":2, "b":1}', "opts": {"sorted": True, "after_comma": 1}},
        {"json": '{"a" :2,"b" :1}', "opts": {"sorted": True, "before_colon": 1}},
        {"json": '{"a": 2,"b": 1}', "opts": {"sorted": True, "after_colon": 1}},
        {"json": '{"a" : 2,"b" : 1}', "opts": {"sorted": True, "before_colon": 1, "after_colon": 1}},
        {"json": '{"a" : 2, "b" : 1}', "opts": {"sorted": True, "before_colon": 1, "after_colon": 1, "after_comma": 1}},
        {"json": '{ "a" : 2, "b" : 1 }', "opts": {"sorted": True, "before_colon": 1, "after_colon": 1, "after_comma": 1, "padding": 1}},
        {"json": '{ "a" : 2, "b" : 1 }', "opts": {"sorted": True, "around_colon": 1, "after_comma": 1, "object_padding": 1}},
        {"json": '{"a" : 2, "b" : 1}', "opts": {"sorted": True, "before_colon": 1, "after_colon": 1, "after_comma": 1, "array_padding": 1}},
        {"json": '{  "a"  :  2, "b"  :  1  }', "opts": {"sorted": True, "around_colon": 2, "after_comma": 1, "padding": 2}},
        {"json": '{  "a":2, "b":1  }', "opts": {"sorted": True, "after_comma": 1, "padding": 2}},
        {"json": '{"b":  1,"a":  2}', "opts": {"after_colon_1": 2}},
        {"json": '{"b"  :  1,"a"  :  2}', "opts": {"around_colon_1": 2}},
        {"json": '{\n  "b":1,\n  "a":2\n}', "opts": {"wrap": True, "around_colon_1": 2}},
        {"json": '{\n  "b": 1,\n  "a": 2\n}', "opts": {"wrap": True, "after_colon": 1}},
        {"json": '{\n  "b": 1,\n  "a": 2\n}', "opts": {"wrap": True, "after_colon_n": 1}},
        {"json": '{"b":1,\n "a":2}', "opts": {"wrap": True, "short": True}},
        {"json": '{"b": 1,\n "a": 2}', "opts": {"wrap": True, "short": True, "after_colon": 1}},
        {"json": '{"b": 1,\n "a": 2}', "opts": {"wrap": True, "short": True, "after_colon_n": 1}},
        {"json": '{"b":1,\n "a":2}', "opts": {"wrap": True, "short": True, "after_colon_1": 1}},
    ]},

    {"value": {"b": 1, "aaa": 2, "cc": 3}, "tests": [
        {"json": '{\n  "b":1,\n  "aaa":2,\n  "cc":3\n}', "opts": {"wrap": True}},
        {"json": '{\n  "b"  :1,\n  "aaa":2,\n  "cc" :3\n}', "opts": {"wrap": True, "aligned": True}},
        {"json": '{"b":1,"aaa":2,"cc":3}', "opts": {"aligned": True}},
        {"json": '{\n  "aaa":2,\n  "b"  :1,\n  "cc" :3\n}', "opts": {"wrap": True, "aligned": True, "sorted": True}},
    ]},

    {"value": {"a": 1}, "tests": [
        {"json": '{"a":1}'},
        {"json": '{\n  "a":1\n}', "opts": {"wrap": True}},
        {"json": '{\n  "a":1\n  }', "opts": {"wrap": True, "indent_last": True}},
        {"json": '{\n "a":1\n }', "opts": {"wrap": True, "indent": " ", "indent_last": True}},
    ]},

    {"value": {"b": 17, "a": 42}, "tests": [
        {"json": '{"a":42,\n "b":17}', "opts": {"wrap": 10, "sorted": True, "short": True}},
        {"json": '{"a":42,\n "b":17}', "opts": {"wrap": 10, "sort": True, "short": True}},
        {"json": '{\n  "a":42,\n  "b":17\n}', "opts": {"wrap": 1, "sorted": True}},
        {"json": '{\n  "a":42,\n  "b":17\n}', "opts": {"wrap": 1, "sort": True}},
        {"json": '{"a":42,"b":17}', "opts": {"wrap": False, "sort": lambda k: k}},
        {"json": '{"b":17,"a":42}', "opts": {"wrap": False, "sort": lambda k, v: v}},
        {"json": '{"a":42,"b":17}', "opts": {"wrap": False, "sort": lambda k, v: -v}},
        {"json": '{"a":42,"b":17}', "opts": {"wrap": False, "sort": lambda k, v, h: 0 if v == max(h.values()) else 1}},
        {"json": '{\n"b":17,\n"a":42\n}', "opts": {"wrap": 1, "indent": "", "sort": lambda k, v: 1 if k == "a" else 0}},
        {"json": '{\n"a":42,\n"b":17\n}', "opts": {"wrap": 1, "indent": "", "sort": lambda k, v: 0 if k == "a" else 1}},
    ]},

    {"value": [1, {"a": 2}, 3], "tests": [
        {"json": '[1,{"a":2},3]'},
        {"json": '[ 1,{ "a":2 },3 ]', "opts": {"padding": 1}},
        {"json": '[ 1, { "a":2 }, 3 ]', "opts": {"padding": 1, "after_comma": 1}},
        {"json": '[\n  1,\n  {\n    "a":2\n  },\n  3\n]', "opts": {"wrap": True}},
        {"json": '[\n  1,\n  {"a":2},\n  3\n]', "opts": {"wrap": 10}},
        {"json": '[\n  1,\n  {\n    "a":2\n    },\n  3\n  ]', "opts": {"wrap": True, "indent_last": True}},
    ]},

    {"value": [1, {"a": 2, "b": 3}, 4], "tests": [
        {"json": '[1,\n {"a":2,\n  "b":3},\n 4]', "opts": {"wrap": 0, "short": True}},
    ]},

    {"value": {"a": 1, "b": [2, 3, 4], "c": 3}, "tests": [
        {"json": '{"a":1,"b":[2,3,4],"c":3}'},
        {"json": '{\n  "a":1,\n  "b":[2,3,4],\n  "c":3\n}', "opts": {"wrap": 10}},
        {"json": '{\n  "a":1,\n  "b":[\n    2,\n    3,\n    4\n  ],\n  "c":3\n}', "opts": {"wrap": True}},
        {"json": '{\n  "a":1,\n  "b":[\n    2,\n    3,\n    4\n    ],\n  "c":3\n  }', "opts": {"wrap": True, "indent_last": True}},
    ]},

    {"value": {"hooo": 42, "whee": ["yaaa", "oooo", "booy"], "zoop": "whoop"}, "tests": [
        {"json": '{"hooo":42,\n "whee":["yaaa",\n         "oooo",\n         "booy"],\n "zoop":"whoop"}', "opts": {"wrap": 20, "short": True}},
    ]},

    {"value": {"a": [{"x": "foo", "y": "jim"}, {"x": "bar", "y": "jam"}]}, "tests": [
        {"json": '{"a":[{"x":"foo",\n       "y":"jim"},\n      {"x":"bar",\n       "y":"jam"}]}', "opts": {"wrap": True, "short": True}},
    ]},

    {"value": {"abcdefghij": [{"abcdefghijklmnop": {}}]}, "tests": [
        {"json": '{"abcdefghij":[{"abcdefghijklmnop":{}}]}'},
        {"json": '{"abcdefghij" : [{"abcdefghijklmnop" : {}}]}', "opts": {"wrap": 1, "short": True, "around_colon_n": 1}},
    ]},

    {"value": {"foo": {}}, "tests": [
        {"json": '{"foo":{}}'},
        {"json": '{"foo":{}}', "opts": {"wrap": False}},
        {"json": '{\n  "foo":{}\n}', "opts": {"wrap": 5}},
        {"json": '{"foo":{}}', "opts": {"wrap": 1, "short": True}},
    ]},

    {"value": ["foo", {}, "bar"], "tests": [
        {"json": '[\n  "foo",\n  {},\n  "bar"\n]', "opts": {"wrap": 1}},
        {"json": '["foo",\n {},\n "bar"]', "opts": {"wrap": 1, "short": True}},
    ]},

    {"value": ["foo", [], "bar"], "tests": [
        {"json": '[\n  "foo",\n  [],\n  "bar"\n]', "opts": {"wrap": 1}},
        {"json": '["foo",\n [],\n "bar"]', "opts": {"wrap": 1, "short": True}},
    ]},

    {"value": ["foo", [{}, [{"foo": []}, 42]], "bar"], "tests": [
        {"json": '["foo",\n [{},\n  [{"foo":[]},\n   42]],\n "bar"]', "opts": {"wrap": 1, "short": True}},
    ]},

    # Deeply nested
    {"value": {"a": {"b": {"c": {"d": {"e": {"f": {"g": {"h": {"i": {"j": {"k": {"l": {"m": 1}}}}}}}}}}}}}, "tests": [
        {"json": '{"a":{"b":{"c":{"d":{"e":{"f":{"g":{"h":{"i":{"j":{"k":{"l":{"m":1}}}}}}}}}}}}}', "opts": {"wrap": False}},
        {"json": '{"a":{"b":{"c":{"d":{"e":{"f":{"g":{"h":{"i":{"j":{"k":{"l":{"m":1}}}}}}}}}}}}}', "opts": {"wrap": 1, "short": True}},
        {"json": '{\n  "a":{\n    "b":{\n      "c":{\n        "d":{\n          "e":{\n            "f":{\n              "g":{\n                "h":{\n                  "i":{\n                    "j":{\n                      "k":{\n                        "l":{\n                          "m":1\n                        }\n                      }\n                    }\n                  }\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}', "opts": {"wrap": 1}},
    ]},

    # Sorting with lambda arity variants (equivalent to Ruby's Issue #27 tests)
    {"value": {"b": 2, "a": 1}, "tests": [
        {"json": '{"b":2,"a":1}', "opts": {"wrap": False}},
        {"json": '{"a":1,"b":2}', "opts": {"wrap": False, "sort": lambda k: k}},
        {"json": '{"a":1,"b":2}', "opts": {"wrap": False, "sort": lambda k, v: k}},
        {"json": '{"a":1,"b":2}', "opts": {"wrap": False, "sort": lambda k, v, o: k}},
        {"json": '{"a":1,"b":2}', "opts": {"wrap": False, "sort": True}},
    ]},

    # Infinity and NaN handling
    {"value": {"inf": math.inf, "neginf": -math.inf, "nan": math.nan}, "tests": [
        {"json": '{"inf":9e9999,"nan":"NaN","neginf":-9e9999}', "opts": {"sort": True}},
    ]},

    # force_floats on arrays
    {"value": [0, 1, 1.1, 1.555555], "tests": [
        {"json": "[0,1,1.1,1.555555]", "opts": {"wrap": False}},
        {"json": "[0.0,1.0,1.1,1.555555]", "opts": {"wrap": False, "force_floats": True}},
        {"json": "[0.000,1.000,1.100,1.556]", "opts": {"wrap": False, "force_floats": True, "decimals": 3}},
        {"json": "[0.0,1.0,1.1,1.556]", "opts": {"wrap": False, "force_floats": True, "decimals": 3, "trim_trailing_zeros": True}},
        {"json": "[0,1,1.1,1.556]", "opts": {"wrap": False, "force_floats": False, "decimals": 3, "trim_trailing_zeros": True}},
    ]},

    # force_floats_in option (using 0.1 like Ruby tests)
    {"value": {"floats": [0, 1, 0.1, 1.555555], "raw": [0, 1, 0.1, 1.555555]}, "tests": [
        {"json": '{"floats":[0,1,0.1,1.555555],"raw":[0,1,0.1,1.555555]}', "opts": {"wrap": False, "sort": True, "force_floats": False}},
        {"json": '{"floats":[0.0,1.0,0.1,1.555555],"raw":[0.0,1.0,0.1,1.555555]}', "opts": {"wrap": False, "sort": True, "force_floats": True}},
        {"json": '{"floats":[0.0,1.0,0.1,1.555555],"raw":[0,1,0.1,1.555555]}', "opts": {"wrap": False, "sort": True, "force_floats_in": ["floats"]}},

        {"json": '{"floats":[0,1,0.100,1.556],"raw":[0,1,0.100,1.556]}', "opts": {"wrap": False, "sort": True, "force_floats": False, "decimals": 3}},
        {"json": '{"floats":[0.000,1.000,0.100,1.556],"raw":[0.000,1.000,0.100,1.556]}', "opts": {"wrap": False, "sort": True, "force_floats": True, "decimals": 3}},
        {"json": '{"floats":[0.000,1.000,0.100,1.556],"raw":[0,1,0.100,1.556]}', "opts": {"wrap": False, "sort": True, "force_floats_in": ["floats"], "decimals": 3}},

        {"json": '{"floats":[0,1,0.1,1.556],"raw":[0,1,0.1,1.556]}', "opts": {"wrap": False, "sort": True, "force_floats": False, "decimals": 3, "trim_trailing_zeros": True}},
        {"json": '{"floats":[0.0,1.0,0.1,1.556],"raw":[0.0,1.0,0.1,1.556]}', "opts": {"wrap": False, "sort": True, "force_floats": True, "decimals": 3, "trim_trailing_zeros": True}},
        {"json": '{"floats":[0.0,1.0,0.1,1.556],"raw":[0,1,0.1,1.556]}', "opts": {"wrap": False, "sort": True, "force_floats_in": ["floats"], "decimals": 3, "trim_trailing_zeros": True}},
    ]},

    # force_floats_in with nested propagation
    {"value": [1, 2, 3, {"a": [4, 5, {"a": 6, "b": 7}], "b": [8, 9, {"a": 10, "b": 11}]}], "tests": [
        {"json": '[1,2,3,{"a":[4,5,{"a":6,"b":7}],"b":[8,9,{"a":10,"b":11}]}]', "opts": {}},
        {"json": '[1.0,2.0,3.0,{"a":[4.0,5.0,{"a":6.0,"b":7.0}],"b":[8.0,9.0,{"a":10.0,"b":11.0}]}]', "opts": {"wrap": False, "force_floats": True}},
        {"json": '[1,2,3,{"a":[4.0,5.0,{"a":6.0,"b":7}],"b":[8,9,{"a":10.0,"b":11}]}]', "opts": {"wrap": False, "force_floats_in": ["a"]}},
    ]},

    # force_floats_in with wrapping (using tabs like Ruby)
    {"value": [1, 2, 3, {"bar": [4, 5, 6], "foo": [7, 8, 9]}], "tests": [
        {"json": "[\n\t1,\n\t2,\n\t3,\n\t{\n\t\t\"bar\":[4,5,6],\n\t\t\"foo\":[7,8,9]\n\t}\n]", "opts": {"wrap": 20, "indent": "\t"}},
        {"json": "[\n\t1,\n\t2,\n\t3,\n\t{\n\t\t\"bar\":[4.0,5.0,6.0],\n\t\t\"foo\":[7,8,9]\n\t}\n]", "opts": {"wrap": 20, "indent": "\t", "force_floats_in": ["bar"]}},
        {"json": "[\n\t1,\n\t2,\n\t3,\n\t{\n\t\t\"bar\":[4,5,6],\n\t\t\"foo\":[7.0,8.0,9.0]\n\t}\n]", "opts": {"wrap": 20, "indent": "\t", "force_floats_in": ["foo"]}},
        {"json": "[\n\t1,\n\t2,\n\t3,\n\t{\n\t\t\"bar\":[4.0,5.0,6.0],\n\t\t\"foo\":[7.0,8.0,9.0]\n\t}\n]", "opts": {"wrap": 20, "indent": "\t", "force_floats_in": ["foo", "bar"]}},
        {"json": "[\n\t1.0,\n\t2.0,\n\t3.0,\n\t{\n\t\t\"bar\":[4.0,5.0,6.0],\n\t\t\"foo\":[7.0,8.0,9.0]\n\t}\n]", "opts": {"wrap": 20, "indent": "\t", "force_floats": True}},
    ]},

    # Issue #32: wrap:true + decimals
    {"value": [1, 2], "tests": [
        {"json": "[\n  1,\n  2\n]", "opts": {"wrap": True, "decimals": 3}},
        {"json": "[\n  1,\n  2\n]", "opts": {"wrap": True, "decimals": 3, "trim_trailing_zeros": True}},
    ]},

    # Issue #33: wrap:true + indent:'' + trim_trailing_zeros
    {"value": [1, 2], "tests": [
        {"json": "[\n1,\n2\n]", "opts": {"wrap": True, "indent": "", "decimals": 3, "trim_trailing_zeros": True}},
        {"json": "[1,\n 2]", "opts": {"wrap": True, "indent": "", "decimals": 3, "trim_trailing_zeros": True, "short": True}},
    ]},
]


# Python-specific test cases
PYTHON_TESTS: list[dict[str, Any]] = [
    # Tuples as arrays
    {"value": (1, 2, 3), "tests": [{"json": "[1,2,3]"}]},
    {"value": (1, (2, 3)), "tests": [{"json": "[1,[2,3]]"}]},

    # Sets as arrays (order may vary)
    {"value": {1}, "tests": [{"json": re.compile(r"\[1\]")}]},

    # Frozensets as arrays
    {"value": frozenset([1]), "tests": [{"json": re.compile(r"\[1\]")}]},

    # Mixed tuple/list
    {"value": [1, (2, 3), 4], "tests": [{"json": "[1,[2,3],4]"}]},

    # None in arrays
    {"value": [1, None, 3], "tests": [{"json": "[1,null,3]"}]},

    # None in objects
    {"value": {"a": None}, "tests": [{"json": '{"a":null}'}]},
]


class CustomJsonClass:
    """Test class with __json__ method."""
    def __init__(self, value: Any) -> None:
        self.value = value

    def __json__(self) -> Any:
        return {"custom": self.value}


CUSTOM_JSON_TESTS: list[dict[str, Any]] = [
    {"value": CustomJsonClass(42), "tests": [{"json": '{"custom":42}'}]},
    {"value": CustomJsonClass("hello"), "tests": [{"json": '{"custom":"hello"}'}]},
    {"value": [CustomJsonClass(1), CustomJsonClass(2)], "tests": [{"json": '[{"custom":1},{"custom":2}]'}]},
]
