import pytest
from hashmap import HashMap
from collections.abc import Iterator

class TestGetValues:

  def test_returns_iterator(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    values = hashmap.get_values()

    assert isinstance(values, Iterator)
    assert iter(values) is values


  def test_contains_all_values_in_order(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert list(hashmap.get_values()) == [
      10,
      20,
      30,
    ]


  def test_reverse_returns_values_in_reverse_order(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert list(hashmap.get_values(reverse=True)) == [
      30,
      20,
      10,
    ]


  @pytest.mark.parametrize("reverse", [False, True])
  def test_empty_hashmap_returns_empty_iterator(
    self,
    empty_hashmap: HashMap[str, int],
    reverse: bool,
  ) -> None:
    assert list(empty_hashmap.get_values(reverse=reverse)) == []


  def test_iterator_is_single_use(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    values = hashmap.get_values()

    assert next(values) == 10
    assert list(values) == [
      20,
      30,
    ]
    assert list(values) == []


  def test_mutable_values_are_returned_by_reference(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    values = mutable_hashmap.get_values()
    first = next(values)

    first.append(100)

    assert mutable_hashmap.get("a") == [
      1,
      2,
      100,
    ]


  def test_reverse_mutable_values_are_returned_by_reference(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    values = mutable_hashmap.get_values(reverse=True)
    last = next(values)

    last.append(100)

    assert mutable_hashmap.get("b") == [
      3,
      4,
      100,
    ]