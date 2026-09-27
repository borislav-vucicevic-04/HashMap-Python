import pytest
from helpers import make_hashmap
from hashmap import HashMap

class TestSort:

  def test_default_sorts_by_value_ascending(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 30,
      "b": 10,
      "c": 20,
    })

    hashmap.sort()

    assert list(hashmap.get_entries()) == [
      ("b", 10),
      ("c", 20),
      ("a", 30),
    ]


  def test_sorts_by_value_descending(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 30,
      "b": 10,
      "c": 20,
    })

    hashmap.sort(
      by="value",
      order="descending",
    )

    assert list(hashmap.get_entries()) == [
      ("a", 30),
      ("c", 20),
      ("b", 10),
    ]


  def test_sorts_by_key_ascending(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "c": 30,
      "a": 10,
      "b": 20,
    })

    hashmap.sort(
      by="key",
      order="ascending",
    )

    assert list(hashmap.get_keys()) == [
      "a",
      "b",
      "c",
    ]


  def test_sorts_by_key_descending(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "c": 30,
      "b": 20,
    })

    hashmap.sort(
      by="key",
      order="descending",
    )

    assert list(hashmap.get_keys()) == [
      "c",
      "b",
      "a",
    ]


  def test_sort_preserves_all_entries(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    before = set(hashmap.get_entries())

    hashmap.sort(
      by="value",
      order="descending",
    )

    assert set(hashmap.get_entries()) == before


  def test_sort_preserves_size(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.sort(
      by="value",
      order="descending",
    )

    assert hashmap.size() == 3


  def test_sort_is_stable(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 20,
      "b": 10,
      "c": 20,
      "d": 10,
    })

    hashmap.sort(
      by="value",
      order="ascending",
    )

    assert list(hashmap.get_entries()) == [
      ("b", 10),
      ("d", 10),
      ("a", 20),
      ("c", 20),
    ]


  def test_empty_hashmap_can_be_sorted(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    empty_hashmap.sort()

    assert empty_hashmap.is_empty() is True


  def test_single_entry_hashmap_can_be_sorted(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
    })

    hashmap.sort(
      by="key",
      order="descending",
    )

    assert list(hashmap.get_entries()) == [
      ("a", 10),
    ]


  def test_invalid_sort_criterion_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.sort(
        by="invalid",  # type: ignore[arg-type]
      )


  def test_invalid_order_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.sort(
        order="invalid",  # type: ignore[arg-type]
      )


  def test_invalid_arguments_do_not_modify_hashmap(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    before = list(hashmap.get_entries())

    with pytest.raises(ValueError):
      hashmap.sort(
        by="invalid",  # type: ignore[arg-type]
      )

    assert list(hashmap.get_entries()) == before


  def test_unorderable_values_raise_type_error(
    self,
  ) -> None:
    hashmap: HashMap[str, object] = make_hashmap({
      "a": 10,
      "b": "twenty",
    })

    with pytest.raises(TypeError):
      hashmap.sort(by="value")


  def test_failed_sort_does_not_replace_internal_order(
    self,
  ) -> None:
    hashmap: HashMap[str, object] = make_hashmap({
      "a": 10,
      "b": "twenty",
    })

    before = list(hashmap.get_entries())

    with pytest.raises(TypeError):
      hashmap.sort(by="value")

    assert list(hashmap.get_entries()) == before