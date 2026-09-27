from helpers import make_hashmap
from hashmap import HashMap
class TestIsSubset:
  def test_proper_subset_returns_true(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
    })

    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 30,
    })

    assert hashmap.issubset(other) is True


  def test_equal_hashmaps_return_true(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 30,
    })

    assert hashmap.issubset(other) is True


  def test_missing_key_returns_false(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
    })

    assert hashmap.issubset(other) is False


  def test_different_value_returns_false(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 999,
    })

    assert hashmap.issubset(other) is False


  def test_empty_is_subset_of_non_empty(
    self,
    hashmap: HashMap[str, int],
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert empty_hashmap.issubset(
      hashmap
    ) is True


  def test_non_empty_is_not_subset_of_empty(
    self,
    hashmap: HashMap[str, int],
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.issubset(
      empty_hashmap
    ) is False


  def test_empty_is_subset_of_empty(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({})

    assert empty_hashmap.issubset(
      other
    ) is True


  def test_hashmap_is_subset_of_itself(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.issubset(
      hashmap
    ) is True


  def test_entry_order_does_not_matter(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
    })

    other: HashMap[str, int] = make_hashmap({
      "c": 30,
      "b": 20,
      "a": 10,
    })

    assert hashmap.issubset(
      other
    ) is True