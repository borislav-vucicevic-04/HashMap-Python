import pytest
from hashmap import HashMap
from helpers import make_hashmap

class TestPopFirst:

  def test_removes_and_returns_first_match_from_left(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 20,
      "d": 30,
    })

    result = hashmap.pop_first(
      lambda key, value:
        value == 20,
    )

    assert result == ("b", 20)
    assert hashmap.has("b") is False


  def test_removes_and_returns_first_match_from_right(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 20,
      "d": 30,
    })

    result = hashmap.pop_first(
      lambda key, value:
        value == 20,
      direction="right",
    )

    assert result == ("c", 20)
    assert hashmap.has("c") is False


  def test_removes_only_one_matching_entry(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 20,
      "b": 20,
      "c": 20,
    })

    hashmap.pop_first(
      lambda key, value:
        value == 20,
    )

    assert hashmap.size() == 2


  def test_returns_none_when_nothing_matches(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.pop_first(
      lambda key, value:
        value > 100,
    )

    assert result is None


  def test_returns_supplied_default_when_nothing_matches(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    default = ("default", 999)

    result = hashmap.pop_first(
      lambda key, value:
        value > 100,
      default=default,
    )

    assert result == default


  def test_no_match_does_not_modify_hashmap(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    before = list(hashmap.get_entries())

    hashmap.pop_first(
      lambda key, value:
        value > 100,
    )

    assert list(hashmap.get_entries()) == before


  def test_empty_hashmap_returns_default(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    default = ("default", 999)

    result = empty_hashmap.pop_first(
      lambda key, value:
        True,
      default=default,
    )

    assert result == default


  def test_rule_exception_propagates(
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
      hashmap.pop_first(rule)


  def test_rule_exception_does_not_modify_hashmap(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    before = list(hashmap.get_entries())

    def rule(
      key: str,
      value: int,
    ) -> bool:
      raise RuntimeError("rule failed")

    with pytest.raises(RuntimeError):
      hashmap.pop_first(rule)

    assert list(hashmap.get_entries()) == before
