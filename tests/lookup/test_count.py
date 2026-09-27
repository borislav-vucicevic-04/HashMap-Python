import pytest
from hashmap import HashMap

class TestCount:

  def test_counts_matching_entries(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.count(
      lambda key, value: value >= 20
    )

    assert result == 2

  def test_rule_can_use_key_and_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.count(
      lambda key, value:
        key != "a" and value >= 20
    )

    assert result == 2

  def test_returns_zero_when_nothing_matches(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.count(
      lambda key, value: value > 100
    )

    assert result == 0

  def test_returns_size_when_everything_matches(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.count(
      lambda key, value: True
    )

    assert result == hashmap.size()

  def test_empty_hashmap_returns_zero(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    result = empty_hashmap.count(
      lambda key, value: True
    )

    assert result == 0

  def test_evaluates_entries_in_iteration_order(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    visited: list[tuple[str, int]] = []

    def rule(
      key: str,
      value: int,
    ) -> bool:
      visited.append((key, value))

      return True

    hashmap.count(rule)

    assert visited == [
      ("a", 10),
      ("b", 20),
      ("c", 30),
    ]

  def test_propagates_rule_exception(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    def rule(
      key: str,
      value: int,
    ) -> bool:
      raise RuntimeError("rule failed")

    with pytest.raises(
      RuntimeError,
      match="rule failed",
    ):
      hashmap.count(rule)