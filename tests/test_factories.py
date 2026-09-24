import pytest
from typing import Any
from hashmap import HashMap


# ==================================================
# TEMPORARY SETUP
# ==================================================

@pytest.fixture(autouse=True)
def allow_partial_hashmap(monkeypatch: pytest.MonkeyPatch) -> None:
  """
  Allow HashMap to be instantiated while the remaining abstract method
  groups are still under development.

  Remove this fixture once HashMap implements the complete interface.
  """

  monkeypatch.setattr(
    HashMap,
    "__abstractmethods__",
    frozenset[str](),
  )


# ==================================================
# FROM DICT
# ==================================================

def test_from_dict_returns_hashmap():
  hashmap = HashMap[str, int].from_dict({
    "a": 1,
    "b": 2,
  })

  assert isinstance(hashmap, HashMap)


def test_from_dict_stores_all_entries():
  hashmap = HashMap[str, int].from_dict({
    "a": 1,
    "b": 2,
    "c": 3,
  })

  assert hashmap._map == { # type: ignore
    "a": 1,
    "b": 2,
    "c": 3,
  }


def test_from_dict_preserves_entry_order():
  hashmap = HashMap[str, int].from_dict({
    "first": 1,
    "second": 2,
    "third": 3,
  })

  assert list(hashmap._map.keys()) == [ # type: ignore
    "first",
    "second",
    "third",
  ]


def test_from_dict_creates_new_internal_dictionary():
  source = {
    "a": 1,
    "b": 2,
  }

  hashmap = HashMap[str, int].from_dict(source)

  assert hashmap._map == source # type: ignore
  assert hashmap._map is not source # type: ignore


def test_from_dict_deep_copies_mutable_values():
  source = {
    "numbers": [1, 2, 3],
  }

  hashmap = HashMap[str, list[int]].from_dict(source) 

  assert hashmap._map["numbers"] == [1, 2, 3] # type: ignore
  assert hashmap._map["numbers"] is not source["numbers"] # type: ignore


def test_from_dict_source_mutation_does_not_affect_hashmap():
  source: dict[str, Any] = {
    "user": {
      "name": "Alice",
      "roles": ["user"],
    },
  }

  hashmap = HashMap[str, dict[str, Any]].from_dict(source)

  source["user"]["name"] = "Bob"
  source["user"]["roles"].append("admin")

  assert hashmap._map == { # type: ignore
    "user": {
      "name": "Alice",
      "roles": ["user"],
    },
  }


def test_from_dict_hashmap_mutation_does_not_affect_source():
  source = {
    "numbers": [1, 2, 3],
  }

  hashmap = HashMap[str, list[int]].from_dict(source)

  hashmap._map["numbers"].append(4) # type: ignore

  assert source == {
    "numbers": [1, 2, 3],
  }


def test_from_dict_deep_copies_multiple_nested_levels():
  source = {
    "settings": {
      "groups": [
        {
          "permissions": ["read"],
        },
      ],
    },
  }

  hashmap = HashMap[str, dict[str, list[dict[str, list[str]]]]].from_dict(source)

  hashmap._map[ # type: ignore
    "settings"
  ]["groups"][0]["permissions"].append("write")

  assert source == {
    "settings": {
      "groups": [
        {
          "permissions": ["read"],
        },
      ],
    },
  }


def test_from_dict_empty_dictionary_creates_empty_hashmap():
  hashmap = HashMap[str, int].from_dict({})

  assert hashmap._map == {} # type: ignore


# ==================================================
# FROM ENTRIES
# ==================================================

def test_from_entries_returns_hashmap():
  hashmap = HashMap[str, int].from_entries([
    ("a", 1),
    ("b", 2),
  ])

  assert isinstance(hashmap, HashMap)


def test_from_entries_stores_all_entries():
  hashmap = HashMap[str, int].from_entries([
    ("a", 1),
    ("b", 2),
    ("c", 3),
  ])

  assert hashmap._map == { # type: ignore
    "a": 1,
    "b": 2,
    "c": 3,
  }


def test_from_entries_preserves_entry_order():
  hashmap = HashMap[str, int].from_entries([
    ("first", 1),
    ("second", 2),
    ("third", 3),
  ])

  assert list(hashmap._map.keys()) == [ # type: ignore
    "first",
    "second",
    "third",
  ]


def test_from_entries_duplicate_key_keeps_last_value():
  hashmap = HashMap[str, int].from_entries([
    ("a", 1),
    ("b", 2),
    ("a", 3),
  ])

  assert hashmap._map == { # type: ignore
    "a": 3,
    "b": 2,
  }


def test_from_entries_deep_copies_mutable_values():
  numbers = [1, 2, 3]

  entries = [
    ("numbers", numbers),
  ]

  hashmap = HashMap[str, list[int]].from_entries(entries)

  assert hashmap._map["numbers"] == [1, 2, 3] # type: ignore
  assert hashmap._map["numbers"] is not numbers # type: ignore


def test_from_entries_source_mutation_does_not_affect_hashmap():
  profile: dict[str, Any] = {
    "name": "Alice",
    "roles": ["user"],
  }

  entries = [
    ("profile", profile),
  ]

  hashmap = HashMap[str, dict[str, Any]].from_entries(entries)

  profile["name"] = "Bob"
  profile["roles"].append("admin")

  assert hashmap._map["profile"] == { # type: ignore
    "name": "Alice",
    "roles": ["user"],
  }


def test_from_entries_hashmap_mutation_does_not_affect_source():
  numbers = [1, 2, 3]

  entries: list[tuple[str, list[int]]] = [
    ("numbers", numbers),
  ]

  hashmap = HashMap[str, list[int]].from_entries(entries)

  hashmap._map["numbers"].append(4) # type: ignore

  assert numbers == [1, 2, 3]


def test_from_entries_empty_list_creates_empty_hashmap():
  hashmap = HashMap[str, int].from_entries([])

  assert hashmap._map == {} # type: ignore


def test_from_entries_raises_type_error_for_unhashable_key():
  entries = [
    (["unhashable"], 1),
  ]

  with pytest.raises(TypeError):
    HashMap[str, int].from_entries(entries) # type: ignore