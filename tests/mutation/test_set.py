import pytest
from hashmap import HashMap
from helpers import make_hashmap


class TestSet:

  def test_inserts_missing_key(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.set("d", 40)

    assert hashmap.includes("d", 40) is True


  def test_replaces_existing_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.set("b", 200)

    assert hashmap.get("b") == 200


  def test_new_entry_is_appended(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.set("d", 40)

    assert list(hashmap.get_keys()) == [
      "a",
      "b",
      "c",
      "d",
    ]


  def test_existing_entry_keeps_position(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.set("b", 200)

    assert list(hashmap.get_keys()) == [
      "a",
      "b",
      "c",
    ]


  def test_stores_value_by_reference(
    self,
  ) -> None:
    hashmap: HashMap[str, list[int]] = make_hashmap({})
    value = [1, 2]

    hashmap.set("a", value)

    value.append(3)

    assert hashmap.get("a") == [
      1,
      2,
      3,
    ]


  def test_none_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.set(
        None,  # type: ignore[arg-type]
        10,
      )


  def test_none_value_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.set(
        "a",
        None,  # type: ignore[arg-type]
      )


  def test_unhashable_key_raises_type_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(TypeError):
      hashmap.set(
        ["unhashable"],  # type: ignore[arg-type]
        10,
      )
