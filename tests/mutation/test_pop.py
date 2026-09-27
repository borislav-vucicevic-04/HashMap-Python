import pytest
from hashmap import HashMap
from helpers import make_hashmap


class TestPop:

  def test_removes_and_returns_existing_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.pop("b")

    assert result == 20
    assert hashmap.has("b") is False


  def test_decreases_size_when_key_exists(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.pop("b")

    assert hashmap.size() == 2


  def test_preserves_order_of_remaining_entries(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.pop("b")

    assert list(hashmap.get_entries()) == [
      ("a", 10),
      ("c", 30),
    ]


  def test_returns_none_when_key_is_missing(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.pop("missing")

    assert result is None


  def test_returns_supplied_default_when_key_is_missing(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.pop(
      "missing",
      100,
    )

    assert result == 100


  def test_missing_key_does_not_modify_hashmap(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    before = list(hashmap.get_entries())

    hashmap.pop(
      "missing",
      100,
    )

    assert list(hashmap.get_entries()) == before


  def test_default_is_not_inserted(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.pop(
      "missing",
      100,
    )

    assert hashmap.has("missing") is False


  def test_existing_value_takes_precedence_over_default(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.pop(
      "a",
      999,
    )

    assert result == 10


  def test_returns_stored_mutable_value_by_reference(
    self,
  ) -> None:
    hashmap: HashMap[str, list[int]] = make_hashmap({
      "a": [1, 2],
    })

    stored = hashmap.get("a")

    assert stored is not None

    result = hashmap.pop("a")

    assert result is stored
    assert hashmap.has("a") is False


  def test_returns_mutable_default_by_reference(
    self,
  ) -> None:
    hashmap: HashMap[str, list[int]] = make_hashmap({})
    default = [1, 2]

    result = hashmap.pop(
      "missing",
      default,
    )

    assert result is default


  def test_none_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.pop(
        None  # type: ignore[arg-type]
      )


  def test_none_key_does_not_modify_hashmap(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    before = list(hashmap.get_entries())

    with pytest.raises(KeyError):
      hashmap.pop(
        None  # type: ignore[arg-type]
      )

    assert list(hashmap.get_entries()) == before


  def test_unhashable_key_raises_type_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(TypeError):
      hashmap.pop(
        ["unhashable"]  # type: ignore[arg-type]
      )


  def test_empty_hashmap_returns_none(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    result = empty_hashmap.pop("missing")

    assert result is None


  def test_empty_hashmap_returns_supplied_default(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    result = empty_hashmap.pop(
      "missing",
      100,
    )

    assert result == 100