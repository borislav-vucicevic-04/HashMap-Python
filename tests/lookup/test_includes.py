import pytest
from hashmap import HashMap
from helpers import make_hashmap, EqualityValue

class TestIncludes:
  def test_returns_true_for_matching_entry(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.includes(
      "a",
      10,
    ) is True

  def test_returns_false_when_value_differs(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.includes(
      "a",
      20,
    ) is False

  def test_returns_false_when_key_is_missing(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.includes(
      "missing",
      10,
    ) is False

  def test_supports_unhashable_values(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    assert mutable_hashmap.includes(
      "a",
      [1, 2],
    ) is True

  def test_uses_equality_comparison(
    self,
  ) -> None:
    hashmap: HashMap[str, EqualityValue] = make_hashmap({
      "a": EqualityValue(10),
    })

    assert hashmap.includes(
      "a",
      EqualityValue(10),
    ) is True

    assert hashmap.includes(
      "a",
      EqualityValue(20),
    ) is False

  def test_none_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.includes(
        None,  # type: ignore[arg-type]
        10,
      )

  def test_none_value_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.includes(
        "a",
        None,  # type: ignore[arg-type]
      )