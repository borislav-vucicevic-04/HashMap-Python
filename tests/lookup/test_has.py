import pytest
from hashmap import HashMap

class TestHas:
  def test_returns_true_for_existing_key(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.has("a") is True

  def test_returns_false_for_missing_key(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.has("missing") is False

  def test_none_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.has(None)  # type: ignore[arg-type]

  def test_unhashable_key_raises_type_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(TypeError):
      hashmap.has(
        ["unhashable"]  # type: ignore[arg-type]
      )