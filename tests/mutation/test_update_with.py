import pytest
from hashmap import HashMap

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
