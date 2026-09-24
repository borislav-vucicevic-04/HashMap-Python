from collections.abc import ItemsView, KeysView, ValuesView

import pytest

from hashmap import HashMap


# ==================================================
# HELPERS
# ==================================================

class EqualityValue:
  def __init__(self, value: int) -> None:
    self.value = value

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, EqualityValue):
      return False

    return self.value == other.value


def make_hashmap[K, V](
  dictionary: dict[K, V],
) -> HashMap[K, V]:
  hashmap: HashMap[K, V] = HashMap[K, V].from_dict(dictionary)

  return hashmap


# ==================================================
# FIXTURES
# ==================================================

@pytest.fixture(autouse=True)
def allow_partial_hashmap(
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  """
  Allow HashMap to be instantiated while other method groups are still
  under development.

  Remove this fixture once HashMap implements the complete interface.
  """

  monkeypatch.setattr(
    HashMap,
    "__abstractmethods__",
    frozenset[str](),
  )


@pytest.fixture
def hashmap() -> HashMap[str, int]:
  return make_hashmap({
    "a": 10,
    "b": 20,
    "c": 30,
  })


@pytest.fixture
def empty_hashmap() -> HashMap[str, int]:
  return make_hashmap({})


@pytest.fixture
def mutable_hashmap() -> HashMap[str, list[int]]:
  return make_hashmap({
    "a": [1, 2],
    "b": [3, 4],
  })


# ==================================================
# GET KEYS
# ==================================================

class TestGetKeys:

  def test_returns_keys_view(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert isinstance(
      hashmap.get_keys(),
      KeysView,
    )


  def test_contains_all_keys_in_order(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert list(hashmap.get_keys()) == [
      "a",
      "b",
      "c",
    ]


  def test_empty_hashmap_returns_empty_view(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert list(empty_hashmap.get_keys()) == []


  def test_returns_live_view(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    keys = hashmap.get_keys()

    hashmap._map["d"] = 40 # type: ignore

    assert list(keys) == [
      "a",
      "b",
      "c",
      "d",
    ]


# ==================================================
# GET VALUES
# ==================================================

class TestGetValues:

  def test_returns_values_view(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert isinstance(
      hashmap.get_values(),
      ValuesView,
    )


  def test_contains_all_values_in_order(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert list(hashmap.get_values()) == [
      10,
      20,
      30,
    ]


  def test_empty_hashmap_returns_empty_view(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert list(empty_hashmap.get_values()) == []


  def test_returns_live_view(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    values = hashmap.get_values()

    hashmap._map["d"] = 40 # type: ignore

    assert list(values) == [
      10,
      20,
      30,
      40,
    ]


  def test_mutable_values_are_returned_by_reference(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    values = mutable_hashmap.get_values()
    first = next(iter(values))

    first.append(100)

    assert mutable_hashmap.get("a") == [
      1,
      2,
      100,
    ]


# ==================================================
# GET ENTRIES
# ==================================================

class TestGetEntries:

  def test_returns_items_view(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert isinstance(
      hashmap.get_entries(),
      ItemsView,
    )


  def test_contains_all_entries_in_order(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert list(hashmap.get_entries()) == [
      ("a", 10),
      ("b", 20),
      ("c", 30),
    ]


  def test_empty_hashmap_returns_empty_view(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert list(empty_hashmap.get_entries()) == []


  def test_returns_live_view(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    entries = hashmap.get_entries()

    hashmap._map["d"] = 40 # type: ignore

    assert list(entries) == [
      ("a", 10),
      ("b", 20),
      ("c", 30),
      ("d", 40),
    ]


  def test_mutable_values_are_returned_by_reference(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    _, value = next(
      iter(mutable_hashmap.get_entries())
    )

    value.append(100)

    assert mutable_hashmap.get("a") == [
      1,
      2,
      100,
    ]


# ==================================================
# SIZE
# ==================================================

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


# ==================================================
# IS EMPTY
# ==================================================

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


# ==================================================
# COUNT
# ==================================================

class TestCount:

  def test_counts_matching_entries(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.count(
      lambda key, value: value >= 20
    )

    assert result == 2


  def test_rule_can_use_key_and_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.count(
      lambda key, value:
        key != "a" and value >= 20
    )

    assert result == 2


  def test_returns_zero_when_nothing_matches(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.count(
      lambda key, value: value > 100
    )

    assert result == 0


  def test_returns_size_when_everything_matches(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.count(
      lambda key, value: True
    )

    assert result == hashmap.size()


  def test_empty_hashmap_returns_zero(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    result = empty_hashmap.count(
      lambda key, value: True
    )

    assert result == 0


  def test_evaluates_entries_in_iteration_order(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    visited: list[tuple[str, int]] = []

    def rule(
      key: str,
      value: int,
    ) -> bool:
      visited.append((key, value))

      return True

    hashmap.count(rule)

    assert visited == [
      ("a", 10),
      ("b", 20),
      ("c", 30),
    ]


  def test_propagates_rule_exception(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    def rule(
      key: str,
      value: int,
    ) -> bool:
      raise RuntimeError("rule failed")

    with pytest.raises(
      RuntimeError,
      match="rule failed",
    ):
      hashmap.count(rule)


# ==================================================
# HAS
# ==================================================

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


# ==================================================
# CONTAINS
# ==================================================

class TestContains:

  def test_returns_true_for_existing_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.contains(20) is True


  def test_returns_false_for_missing_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.contains(100) is False


  def test_empty_hashmap_returns_false(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert empty_hashmap.contains(10) is False


  def test_duplicate_values_are_supported(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 10,
      "c": 20,
    })

    assert hashmap.contains(10) is True


  def test_unhashable_values_are_supported(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    assert mutable_hashmap.contains(
      [1, 2]
    ) is True

    assert mutable_hashmap.contains(
      [100]
    ) is False


  def test_uses_equality_comparison(
    self,
  ) -> None:
    hashmap: HashMap[str, EqualityValue] = make_hashmap({
      "a": EqualityValue(10),
    })

    assert hashmap.contains(
      EqualityValue(10)
    ) is True

    assert hashmap.contains(
      EqualityValue(20)
    ) is False


  def test_none_value_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.contains(None)  # type: ignore[arg-type]


# ==================================================
# INCLUDES
# ==================================================

class TestIncludes:

  def test_returns_true_for_matching_entry(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.includes(
      "a",
      10,
    ) is True


  def test_returns_false_when_value_differs(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.includes(
      "a",
      20,
    ) is False


  def test_returns_false_when_key_is_missing(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.includes(
      "missing",
      10,
    ) is False


  def test_supports_unhashable_values(
    self,
    mutable_hashmap: HashMap[str, list[int]],
  ) -> None:
    assert mutable_hashmap.includes(
      "a",
      [1, 2],
    ) is True


  def test_uses_equality_comparison(
    self,
  ) -> None:
    hashmap: HashMap[str, EqualityValue] = make_hashmap({
      "a": EqualityValue(10),
    })

    assert hashmap.includes(
      "a",
      EqualityValue(10),
    ) is True

    assert hashmap.includes(
      "a",
      EqualityValue(20),
    ) is False


  def test_none_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.includes(
        None,  # type: ignore[arg-type]
        10,
      )


  def test_none_value_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.includes(
        "a",
        None,  # type: ignore[arg-type]
      )


# ==================================================
# GET
# ==================================================

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


# ==================================================
# IS SUPERSET
# ==================================================

class TestIsSuperset:

  def test_proper_superset_returns_true(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
    })

    assert hashmap.issuperset(other) is True


  def test_equal_hashmaps_return_true(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 30,
    })

    assert hashmap.issuperset(other) is True


  def test_missing_key_returns_false(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "d": 40,
    })

    assert hashmap.issuperset(other) is False


  def test_different_value_returns_false(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 999,
    })

    assert hashmap.issuperset(other) is False


  def test_every_hashmap_is_superset_of_empty_hashmap(
    self,
    hashmap: HashMap[str, int],
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.issuperset(
      empty_hashmap
    ) is True


  def test_empty_is_not_superset_of_non_empty(
    self,
    hashmap: HashMap[str, int],
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert empty_hashmap.issuperset(
      hashmap
    ) is False


  def test_empty_is_superset_of_empty(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({})

    assert empty_hashmap.issuperset(
      other
    ) is True


  def test_hashmap_is_superset_of_itself(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.issuperset(
      hashmap
    ) is True


  def test_entry_order_does_not_matter(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "c": 30,
      "a": 10,
    })

    assert hashmap.issuperset(
      other
    ) is True


# ==================================================
# IS SUBSET
# ==================================================

class TestIsSubset:

  def test_proper_subset_returns_true(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
    })

    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 30,
    })

    assert hashmap.issubset(other) is True


  def test_equal_hashmaps_return_true(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 30,
    })

    assert hashmap.issubset(other) is True


  def test_missing_key_returns_false(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
    })

    assert hashmap.issubset(other) is False


  def test_different_value_returns_false(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 999,
    })

    assert hashmap.issubset(other) is False


  def test_empty_is_subset_of_non_empty(
    self,
    hashmap: HashMap[str, int],
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert empty_hashmap.issubset(
      hashmap
    ) is True


  def test_non_empty_is_not_subset_of_empty(
    self,
    hashmap: HashMap[str, int],
    empty_hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.issubset(
      empty_hashmap
    ) is False


  def test_empty_is_subset_of_empty(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    other: HashMap[str, int] = make_hashmap({})

    assert empty_hashmap.issubset(
      other
    ) is True


  def test_hashmap_is_subset_of_itself(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    assert hashmap.issubset(
      hashmap
    ) is True


  def test_entry_order_does_not_matter(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
    })

    other: HashMap[str, int] = make_hashmap({
      "c": 30,
      "b": 20,
      "a": 10,
    })

    assert hashmap.issubset(
      other
    ) is True