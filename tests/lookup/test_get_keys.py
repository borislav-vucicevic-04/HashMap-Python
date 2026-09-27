import pytest
from hashmap import HashMap
from collections.abc import Iterator

class TestGetKeys:
  def test_returns_iterator(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    keys = hashmap.get_keys()

    assert isinstance(keys, Iterator)
    assert iter(keys) is keys


  def test_contains_all_keys_in_order(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert list(hashmap.get_keys()) == [
      "a",
      "b",
      "c",
    ]

  def test_reverse_returns_keys_in_reverse_order(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert list(hashmap.get_keys(reverse=True)) == [
      "c",
      "b",
      "a",
    ]

  @pytest.mark.parametrize("reverse", [False, True])
  def test_empty_hashmap_returns_empty_iterator(
    self,
    empty_hashmap: HashMap[str, int],
    reverse: bool,
  ) -> None:
    assert list(empty_hashmap.get_keys(reverse=reverse)) == []

  def test_iterator_is_single_use(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    keys = hashmap.get_keys()

    assert next(keys) == "a"
    assert list(keys) == [
      "b",
      "c",
    ]
    assert list(keys) == []
