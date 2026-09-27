import pytest
from helpers import make_hashmap, EqualityValue
from hashmap import HashMap

class TestContains:
  def test_returns_true_for_existing_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.contains(20) is True

  def test_returns_false_for_missing_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.contains(100) is False

  def test_empty_hashmap_returns_false(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert empty_hashmap.contains(10) is False

  def test_duplicate_values_are_supported(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 10,
      "c": 20,
    })

    assert hashmap.contains(10) is True

  def test_unhashable_values_are_supported(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    assert mutable_hashmap.contains(
      [1, 2]
    ) is True

    assert mutable_hashmap.contains(
      [100]
    ) is False

  def test_uses_equality_comparison(
    self,
  ) -> None:
    hashmap: HashMap[str, EqualityValue] = make_hashmap({
      "a": EqualityValue(10),
    })

    assert hashmap.contains(
      EqualityValue(10)
    ) is True

    assert hashmap.contains(
      EqualityValue(20)
    ) is False

  def test_none_value_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.contains(None)  # type: ignore[arg-type]