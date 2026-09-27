import pytest
from hashmap import HashMap
from collections.abc import Iterator

class TestGetEntries:

  def test_returns_iterator(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    entries = hashmap.get_entries()

    assert isinstance(entries, Iterator)
    assert iter(entries) is entries


  def test_contains_all_entries_in_order(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert list(hashmap.get_entries()) == [
      ("a", 10),
      ("b", 20),
      ("c", 30),
    ]


  def test_reverse_returns_entries_in_reverse_order(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert list(hashmap.get_entries(reverse=True)) == [
      ("c", 30),
      ("b", 20),
      ("a", 10),
    ]


  @pytest.mark.parametrize("reverse", [False, True])
  def test_empty_hashmap_returns_empty_iterator(
    self,
    empty_hashmap: HashMap[str, int],
    reverse: bool,
  ) -> None:
    assert list(empty_hashmap.get_entries(reverse=reverse)) == []


  def test_iterator_is_single_use(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    entries = hashmap.get_entries()

    assert next(entries) == ("a", 10)
    assert list(entries) == [
      ("b", 20),
      ("c", 30),
    ]
    assert list(entries) == []


  def test_mutable_values_are_returned_by_reference(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    _, value = next(mutable_hashmap.get_entries())

    value.append(100)

    assert mutable_hashmap.get("a") == [
      1,
      2,
      100,
    ]


  def test_reverse_mutable_values_are_returned_by_reference(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    key, value = next(
      mutable_hashmap.get_entries(reverse=True)
    )

    value.append(100)

    assert key == "b"
    assert mutable_hashmap.get("b") == [
      3,
      4,
      100,
    ]