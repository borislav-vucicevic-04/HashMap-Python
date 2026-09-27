from hashmap import HashMap

class TestIsEmpty:

  def test_returns_false_when_entries_exist(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.is_empty() is False


  def test_returns_true_when_empty(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert empty_hashmap.is_empty() is True