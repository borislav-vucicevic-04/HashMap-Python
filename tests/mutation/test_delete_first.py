import pytest
from hashmap import HashMap
from helpers import make_hashmap

class TestDeleteFirst:

  def test_deletes_first_match_from_left(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 20,
      "d": 30,
    })

    hashmap.delete_first(
      lambda key, value:
        value == 20,
    )

    assert list(hashmap.get_entries()) == [
      ("a", 10),
      ("c", 20),
      ("d", 30),
    ]


  def test_deletes_first_match_from_right(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 20,
      "d": 30,
    })

    hashmap.delete_first(
      lambda key, value:
        value == 20,
      direction="right",
    )

    assert list(hashmap.get_entries()) == [
      ("a", 10),
      ("b", 20),
      ("d", 30),
    ]


  def test_removes_only_one_matching_entry(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 20,
      "d": 20,
    })

    hashmap.delete_first(
      lambda key, value:
        value == 20,
    )

    assert hashmap.count(
      lambda key, value:
        value == 20,
    ) == 2


  def test_rule_can_use_key_and_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.delete_first(
      lambda key, value:
        key == "b" and value == 20,
    )

    assert hashmap.has("b") is False


  def test_no_match_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.delete_first(
        lambda key, value:
          value > 100,
      )


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
      hashmap.delete_first(rule)


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
      hashmap.delete_first(rule)

    assert list(hashmap.get_entries()) == before
