import pytest
from hashmap import HashMap
from typing import Any

class TestFromEntries:
  def test_from_entries_returns_hashmap(self):
    hashmap = HashMap[str, int].from_entries([
      ("a", 1),
      ("b", 2),
    ])

    assert isinstance(hashmap, HashMap)


  def test_from_entries_stores_all_entries(self):
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


  def test_from_entries_preserves_entry_order(self):
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


  def test_from_entries_duplicate_key_keeps_last_value(self):
    hashmap = HashMap[str, int].from_entries([
      ("a", 1),
      ("b", 2),
      ("a", 3),
    ])

    assert hashmap._map == { # type: ignore
      "a": 3,
      "b": 2,
    }


  def test_from_entries_deep_copies_mutable_values(self):
    numbers = [1, 2, 3]

    entries = [
      ("numbers", numbers),
    ]

    hashmap = HashMap[str, list[int]].from_entries(entries)

    assert hashmap._map["numbers"] == [1, 2, 3] # type: ignore
    assert hashmap._map["numbers"] is not numbers # type: ignore


  def test_from_entries_source_mutation_does_not_affect_hashmap(self):
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


  def test_from_entries_hashmap_mutation_does_not_affect_source(self):
    numbers = [1, 2, 3]

    entries: list[tuple[str, list[int]]] = [
      ("numbers", numbers),
    ]

    hashmap = HashMap[str, list[int]].from_entries(entries)

    hashmap._map["numbers"].append(4) # type: ignore

    assert numbers == [1, 2, 3]


  def test_from_entries_empty_list_creates_empty_hashmap(self):
    hashmap = HashMap[str, int].from_entries([])

    assert hashmap._map == {} # type: ignore


  def test_from_entries_raises_type_error_for_unhashable_key(self):
    entries = [
      (["unhashable"], 1),
    ]

    with pytest.raises(TypeError):
      HashMap[str, int].from_entries(entries) # type: ignore