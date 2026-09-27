import pytest
from hashmap import HashMap

class TestDelete:

  def test_deletes_existing_entry(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.delete("b")

    assert hashmap.has("b") is False


  def test_decreases_size(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.delete("b")

    assert hashmap.size() == 2


  def test_preserves_order_of_remaining_entries(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.delete("b")

    assert list(hashmap.get_entries()) == [
      ("a", 10),
      ("c", 30),
    ]


  def test_missing_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.delete("missing")


  def test_none_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.delete(
        None  # type: ignore[arg-type]
      )


  def test_failed_delete_does_not_modify_hashmap(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    before = list(hashmap.get_entries())

    with pytest.raises(KeyError):
      hashmap.delete("missing")

    assert list(hashmap.get_entries()) == before
