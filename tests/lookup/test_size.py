from hashmap import HashMap

class TestSize:

  def test_returns_number_of_entries(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.size() == 3


  def test_empty_hashmap_has_size_zero(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert empty_hashmap.size() == 0