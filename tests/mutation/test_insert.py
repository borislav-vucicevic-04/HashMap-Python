import pytest
from hashmap import HashMap
from helpers import make_hashmap

class TestInsert:
  def test_inserts_new_entry(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.insert("d", 40)

    assert hashmap.includes("d", 40) is True


  def test_increases_size(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.insert("d", 40)

    assert hashmap.size() == 4


  def test_appends_entry_to_end(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.insert("d", 40)

    assert list(hashmap.get_entries()) == [
      ("a", 10),
      ("b", 20),
      ("c", 30),
      ("d", 40),
    ]


  def test_stores_value_by_reference(
    self,
  ) -> None:
    hashmap: HashMap[str, list[int]] = make_hashmap({})
    value = [1, 2]

    hashmap.insert("a", value)

    value.append(3)

    assert hashmap.get("a") == [
      1,
      2,
      3,
    ]


  def test_existing_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.insert("a", 100)


  def test_existing_key_failure_does_not_modify_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.insert("a", 100)

    assert hashmap.get("a") == 10


  def test_none_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.insert(
        None,  # type: ignore[arg-type]
        40,
      )


  def test_none_value_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.insert(
        "d",
        None,  # type: ignore[arg-type]
      )


  def test_unhashable_key_raises_type_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(TypeError):
      hashmap.insert(
        ["unhashable"],  # type: ignore[arg-type]
        40,
      )
