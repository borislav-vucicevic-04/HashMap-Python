import pytest
from hashmap import HashMap
from helpers import make_hashmap

class TestUpdate:
  def test_replaces_existing_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.update("b", 200)

    assert hashmap.get("b") == 200


  def test_does_not_change_size(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.update("b", 200)

    assert hashmap.size() == 3


  def test_preserves_entry_position(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.update("b", 200)

    assert list(hashmap.get_entries()) == [
      ("a", 10),
      ("b", 200),
      ("c", 30),
    ]


  def test_stores_new_value_by_reference(
    self,
  ) -> None:
    hashmap: HashMap[str, list[int]] = make_hashmap({
      "a": [1],
    })

    value = [2, 3]

    hashmap.update("a", value)

    value.append(4)

    assert hashmap.get("a") == [
      2,
      3,
      4,
    ]


  def test_missing_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.update("missing", 100)


  def test_none_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.update(
        None,  # type: ignore[arg-type]
        100,
      )


  def test_none_value_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.update(
        "a",
        None,  # type: ignore[arg-type]
      )


  def test_failed_update_does_not_modify_hashmap(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    before = list(hashmap.get_entries())

    with pytest.raises(KeyError):
      hashmap.update("missing", 100)

    assert list(hashmap.get_entries()) == before
