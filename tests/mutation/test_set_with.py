import pytest
from hashmap import HashMap

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
