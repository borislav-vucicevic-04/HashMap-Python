import pytest
from hashmap import HashMap
from helpers import make_hashmap

class TestGet:
  def test_returns_existing_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.get("a") == 10

  def test_missing_key_returns_none(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.get("missing") is None

  def test_missing_key_returns_supplied_default(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.get(
      "missing",
      100,
    ) == 100

  def test_returns_mutable_value_by_reference(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    value = mutable_hashmap.get("a")

    assert value is not None

    value.append(100)

    assert mutable_hashmap.get("a") == [
      1,
      2,
      100,
    ]

  def test_returns_default_by_reference(
    self,
  ) -> None:
    hashmap: HashMap[str, list[int]] = make_hashmap({})
    default = [1, 2]

    result = hashmap.get(
      "missing",
      default,
    )

    assert result is default

  def test_default_is_not_inserted(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    empty_hashmap.get(
      "missing",
      100,
    )

    assert empty_hashmap.has("missing") is False
    assert empty_hashmap.size() == 0

  def test_none_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.get(
        None  # type: ignore[arg-type]
      )

  def test_unhashable_key_raises_type_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(TypeError):
      hashmap.get(
        ["unhashable"]  # type: ignore[arg-type]
      )