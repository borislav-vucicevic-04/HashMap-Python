from hashmap import HashMap
from typing import Any

class TestFromDict:
  def test_from_dict_returns_hashmap(self):
    hashmap = HashMap[str, int].from_dict({
      "a": 1,
      "b": 2,
    })

    assert isinstance(hashmap, HashMap)


  def test_from_dict_stores_all_entries(self):
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


  def test_from_dict_preserves_entry_order(self):
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


  def test_from_dict_creates_new_internal_dictionary(self):
    source = {
      "a": 1,
      "b": 2,
    }

    hashmap = HashMap[str, int].from_dict(source)

    assert hashmap._map == source # type: ignore
    assert hashmap._map is not source # type: ignore


  def test_from_dict_deep_copies_mutable_values(self):
    source = {
      "numbers": [1, 2, 3],
    }

    hashmap = HashMap[str, list[int]].from_dict(source) 

    assert hashmap._map["numbers"] == [1, 2, 3] # type: ignore
    assert hashmap._map["numbers"] is not source["numbers"] # type: ignore


  def test_from_dict_source_mutation_does_not_affect_hashmap(self):
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


  def test_from_dict_hashmap_mutation_does_not_affect_source(self):
    source = {
      "numbers": [1, 2, 3],
    }

    hashmap = HashMap[str, list[int]].from_dict(source)

    hashmap._map["numbers"].append(4) # type: ignore

    assert source == {
      "numbers": [1, 2, 3],
    }


  def test_from_dict_deep_copies_multiple_nested_levels(self):
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


  def test_from_dict_empty_dictionary_creates_empty_hashmap(self):
    hashmap = HashMap[str, int].from_dict({})

    assert hashmap._map == {} # type: ignore