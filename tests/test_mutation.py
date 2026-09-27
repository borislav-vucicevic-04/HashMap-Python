import pytest

from hashmap import HashMap


# ==================================================
# HELPERS
# ==================================================

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


# ==================================================
# INSERT
# ==================================================

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


# ==================================================
# UPDATE
# ==================================================

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


# ==================================================
# UPDATE WITH
# ==================================================

class TestUpdateWith:

  def test_updates_using_handler(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.update_with(
      "a",
      5,
      lambda old_value, new_value:
        old_value + new_value,
    )

    assert hashmap.get("a") == 15


  def test_handler_receives_old_then_new_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    received: list[tuple[int, int]] = []

    def handler(
      old_value: int,
      new_value: int,
    ) -> int:
      received.append((
        old_value,
        new_value,
      ))

      return new_value

    hashmap.update_with(
      "b",
      99,
      handler,
    )

    assert received == [
      (20, 99),
    ]


  def test_preserves_entry_position(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.update_with(
      "b",
      5,
      lambda old_value, new_value:
        old_value + new_value,
    )

    assert list(hashmap.get_keys()) == [
      "a",
      "b",
      "c",
    ]


  def test_missing_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.update_with(
        "missing",
        10,
        lambda old_value, new_value:
          old_value + new_value,
      )


  def test_handler_not_called_when_key_is_missing(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    called = False

    def handler(
      old_value: int,
      new_value: int,
    ) -> int:
      nonlocal called
      called = True

      return new_value

    with pytest.raises(KeyError):
      hashmap.update_with(
        "missing",
        10,
        handler,
      )

    assert called is False


  def test_none_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.update_with(
        None,  # type: ignore[arg-type]
        10,
        lambda old_value, new_value:
          old_value + new_value,
      )


  def test_none_value_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.update_with(
        "a",
        None,  # type: ignore[arg-type]
        lambda old_value, new_value:
          old_value + new_value,
      )


  def test_handler_returning_none_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    def handler(
      old_value: int,
      new_value: int,
    ) -> int:
      return None  # type: ignore[return-value]

    with pytest.raises(ValueError):
      hashmap.update_with(
        "a",
        10,
        handler,
      )


  def test_none_handler_result_does_not_modify_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    def handler(
      old_value: int,
      new_value: int,
    ) -> int:
      return None  # type: ignore[return-value]

    with pytest.raises(ValueError):
      hashmap.update_with(
        "a",
        100,
        handler,
      )

    assert hashmap.get("a") == 10


  def test_handler_exception_propagates(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    def handler(
      old_value: int,
      new_value: int,
    ) -> int:
      raise RuntimeError("handler failed")

    with pytest.raises(
      RuntimeError,
      match="handler failed",
    ):
      hashmap.update_with(
        "a",
        100,
        handler,
      )


  def test_handler_exception_does_not_modify_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    def handler(
      old_value: int,
      new_value: int,
    ) -> int:
      raise RuntimeError("handler failed")

    with pytest.raises(RuntimeError):
      hashmap.update_with(
        "a",
        100,
        handler,
      )

    assert hashmap.get("a") == 10


# ==================================================
# SET
# ==================================================

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


# ==================================================
# SET WITH
# ==================================================

class TestSetWith:

  def test_updates_existing_entry_using_handler(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.set_with(
      "a",
      5,
      lambda old_value, new_value:
        (
          new_value
          if old_value is None
          else old_value + new_value
        ),
    )

    assert hashmap.get("a") == 15


  def test_existing_entry_handler_receives_old_then_new_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    received: list[tuple[int | None, int]] = []

    def handler(
      old_value: int | None,
      new_value: int,
    ) -> int:
      received.append((
        old_value,
        new_value,
      ))

      return new_value

    hashmap.set_with(
      "b",
      99,
      handler,
    )

    assert received == [
      (20, 99),
    ]


  def test_inserts_missing_entry_using_handler(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.set_with(
      "d",
      40,
      lambda old_value, new_value:
        (
          new_value
          if old_value is None
          else old_value + new_value
        ),
    )

    assert hashmap.get("d") == 40


  def test_missing_entry_handler_receives_none(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    received: list[tuple[int | None, int]] = []

    def handler(
      old_value: int | None,
      new_value: int,
    ) -> int:
      received.append((
        old_value,
        new_value,
      ))

      return new_value

    hashmap.set_with(
      "d",
      40,
      handler,
    )

    assert received == [
      (None, 40),
    ]


  def test_none_key_raises_key_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(KeyError):
      hashmap.set_with(
        None,  # type: ignore[arg-type]
        10,
        lambda old_value, new_value:
          new_value,
      )


  def test_none_value_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.set_with(
        "a",
        None,  # type: ignore[arg-type]
        lambda old_value, new_value:
          new_value,
      )


  def test_handler_returning_none_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    def handler(
      old_value: int | None,
      new_value: int,
    ) -> int:
      return None  # type: ignore[return-value]

    with pytest.raises(ValueError):
      hashmap.set_with(
        "a",
        100,
        handler,
      )


  def test_none_handler_result_does_not_modify_existing_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    def handler(
      old_value: int | None,
      new_value: int,
    ) -> int:
      return None  # type: ignore[return-value]

    with pytest.raises(ValueError):
      hashmap.set_with(
        "a",
        100,
        handler,
      )

    assert hashmap.get("a") == 10


  def test_handler_exception_propagates(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    def handler(
      old_value: int | None,
      new_value: int,
    ) -> int:
      raise RuntimeError("handler failed")

    with pytest.raises(
      RuntimeError,
      match="handler failed",
    ):
      hashmap.set_with(
        "a",
        100,
        handler,
      )


# ==================================================
# DELETE
# ==================================================

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


# ==================================================
# DELETE FIRST
# ==================================================

class TestDeleteFirst:

  def test_deletes_first_match_from_left(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 20,
      "d": 30,
    })

    hashmap.delete_first(
      lambda key, value:
        value == 20,
    )

    assert list(hashmap.get_entries()) == [
      ("a", 10),
      ("c", 20),
      ("d", 30),
    ]


  def test_deletes_first_match_from_right(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 20,
      "d": 30,
    })

    hashmap.delete_first(
      lambda key, value:
        value == 20,
      direction="right",
    )

    assert list(hashmap.get_entries()) == [
      ("a", 10),
      ("b", 20),
      ("d", 30),
    ]


  def test_removes_only_one_matching_entry(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 20,
      "d": 20,
    })

    hashmap.delete_first(
      lambda key, value:
        value == 20,
    )

    assert hashmap.count(
      lambda key, value:
        value == 20,
    ) == 2


  def test_rule_can_use_key_and_value(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    hashmap.delete_first(
      lambda key, value:
        key == "b" and value == 20,
    )

    assert hashmap.has("b") is False


  def test_no_match_raises_value_error(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    with pytest.raises(ValueError):
      hashmap.delete_first(
        lambda key, value:
          value > 100,
      )


  def test_rule_exception_propagates(
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
      hashmap.delete_first(rule)


  def test_rule_exception_does_not_modify_hashmap(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    before = list(hashmap.get_entries())

    def rule(
      key: str,
      value: int,
    ) -> bool:
      raise RuntimeError("rule failed")

    with pytest.raises(RuntimeError):
      hashmap.delete_first(rule)

    assert list(hashmap.get_entries()) == before


# ==================================================
# POP FIRST
# ==================================================

class TestPopFirst:

  def test_removes_and_returns_first_match_from_left(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 20,
      "d": 30,
    })

    result = hashmap.pop_first(
      lambda key, value:
        value == 20,
    )

    assert result == ("b", 20)
    assert hashmap.has("b") is False


  def test_removes_and_returns_first_match_from_right(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 10,
      "b": 20,
      "c": 20,
      "d": 30,
    })

    result = hashmap.pop_first(
      lambda key, value:
        value == 20,
      direction="right",
    )

    assert result == ("c", 20)
    assert hashmap.has("c") is False


  def test_removes_only_one_matching_entry(
    self,
  ) -> None:
    hashmap: HashMap[str, int] = make_hashmap({
      "a": 20,
      "b": 20,
      "c": 20,
    })

    hashmap.pop_first(
      lambda key, value:
        value == 20,
    )

    assert hashmap.size() == 2


  def test_returns_none_when_nothing_matches(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    result = hashmap.pop_first(
      lambda key, value:
        value > 100,
    )

    assert result is None


  def test_returns_supplied_default_when_nothing_matches(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    default = ("default", 999)

    result = hashmap.pop_first(
      lambda key, value:
        value > 100,
      default=default,
    )

    assert result == default


  def test_no_match_does_not_modify_hashmap(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    before = list(hashmap.get_entries())

    hashmap.pop_first(
      lambda key, value:
        value > 100,
    )

    assert list(hashmap.get_entries()) == before


  def test_empty_hashmap_returns_default(
    self,
    empty_hashmap: HashMap[str, int],
  ) -> None:
    default = ("default", 999)

    result = empty_hashmap.pop_first(
      lambda key, value:
        True,
      default=default,
    )

    assert result == default


  def test_rule_exception_propagates(
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
      hashmap.pop_first(rule)


  def test_rule_exception_does_not_modify_hashmap(
    self,
    hashmap: HashMap[str, int],
  ) -> None:
    before = list(hashmap.get_entries())

    def rule(
      key: str,
      value: int,
    ) -> bool:
      raise RuntimeError("rule failed")

    with pytest.raises(RuntimeError):
      hashmap.pop_first(rule)

    assert list(hashmap.get_entries()) == before


# ==================================================
# SORT
# ==================================================

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