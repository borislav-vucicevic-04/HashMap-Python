import pytest
from hashmap import HashMap
from helpers import make_hashmap

def create_other_map() -> HashMap[str, int]:
  return make_hashmap({
    "e": 40,
    "d": 50,
    "f": 60
  })

class TestAdd:
  def test_entries_added(self, hashmap: HashMap[str, int]):
    other: HashMap[str, int] = create_other_map()
    hashmap.add(other)
    assert hashmap.issuperset(other) is True

  def test_existing_entries_unchanged(
    self,
    hashmap: HashMap[str, int]
  ):
    original_entries = list(hashmap.get_entries())

    other: HashMap[str, int] = create_other_map()

    hashmap.add(other)

    assert list(hashmap.get_entries())[:3] == original_entries

  def test_size_increases_by_others_size(
    self,
    hashmap: HashMap[str, int]
  ):
    original_size = hashmap.size()
    other = create_other_map()

    hashmap.add(other)

    assert hashmap.size() == (original_size + other.size())

  def test_empty_sources_leaves_target_unchanged(
      self,
      hashmap: HashMap[str, int]
  ):
    other: HashMap[str, int] = make_hashmap({})
    hashmap_entries = list(hashmap.get_entries())

    hashmap.add(other)

    assert hashmap_entries == list(hashmap.get_entries())

  def test_source_remains_unchanged_after_success(
    self,
    hashmap: HashMap[str, int]
  ):
    other: HashMap[str, int] = create_other_map()
    other_entries = list(other.get_entries())

    hashmap.add(other)

    assert other_entries == list(other.get_entries())

  def test_mutable_added_by_reference(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    other: HashMap[str, list[int]] = make_hashmap({
      "c": [5, 6],
    })

    source_value = other.get("c")

    assert source_value is not None

    mutable_hashmap.add(other)

    target_value = mutable_hashmap.get("c")

    assert target_value is source_value

    source_value.append(7)

    assert mutable_hashmap.get("c") is source_value
    assert mutable_hashmap.get("c") == [5, 6, 7]

  def test_duplicate_raises_key_error(
    self,
    hashmap: HashMap[str, int]
  ):
    other = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 30,
    })

    with pytest.raises(KeyError):
      hashmap.add(other)

  def test_operation_fails_atomically_on_colision(
    self,
    hashmap: HashMap[str, int]
  ):
    other = make_hashmap({
      "e": 10,
      "b": 20,
      "d": 30,
    })

    entries = list(hashmap.get_entries())

    with pytest.raises(KeyError):
      hashmap.add(other)

    assert entries == list(hashmap.get_entries())


