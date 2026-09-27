from hashmap import HashMap
from helpers import make_hashmap

class TestIsSuperset:
  def test_proper_superset_returns_true(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
    })

    assert hashmap.issuperset(other) is True


  def test_equal_hashmaps_return_true(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 30,
    })

    assert hashmap.issuperset(other) is True


  def test_missing_key_returns_false(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "d": 40,
    })

    assert hashmap.issuperset(other) is False


  def test_different_value_returns_false(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 999,
    })

    assert hashmap.issuperset(other) is False


  def test_every_hashmap_is_superset_of_empty_hashmap(
    self,
    hashmap: HashMap[str, int],
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.issuperset(
      empty_hashmap
    ) is True


  def test_empty_is_not_superset_of_non_empty(
    self,
    hashmap: HashMap[str, int],
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert empty_hashmap.issuperset(
      hashmap
    ) is False


  def test_empty_is_superset_of_empty(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({})

    assert empty_hashmap.issuperset(
      other
    ) is True


  def test_hashmap_is_superset_of_itself(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.issuperset(
      hashmap
    ) is True


  def test_entry_order_does_not_matter(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "c": 30,
      "a": 10,
    })

    assert hashmap.issuperset(
      other
    ) is True