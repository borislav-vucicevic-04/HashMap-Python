import pytest
import helpers
from hashmap import HashMap


@pytest.fixture(autouse=True)
def allow_partial_hashmap(
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  monkeypatch.setattr(
    HashMap,
    "__abstractmethods__",
    frozenset[str](),
  )

@pytest.fixture
def hashmap() -> HashMap[str, int]:
  return helpers.make_hashmap({
    "a": 10,
    "b": 20,
    "c": 30,
  })

@pytest.fixture
def empty_hashmap() -> HashMap[str, int]:
  return helpers.make_hashmap({})

@pytest.fixture
def mutable_hashmap() -> HashMap[str, list[int]]:
  return helpers.make_hashmap({
    "a": [1, 2],
    "b": [3, 4],
  })