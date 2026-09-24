import pickle
from .interface import HashMapInterface
from typing import Self

class Factories[K, V](HashMapInterface[K, V]):
  @classmethod
  def from_dict(cls, dictionary: dict[K, V]) -> Self:
    instance = cls()

    instance._map = pickle.loads(pickle.dumps(dictionary, protocol=pickle.HIGHEST_PROTOCOL))

    return instance
  
  @classmethod
  def from_entries(cls, entries: list[tuple[K, V]]) -> Self:
    internal_map = dict(entries)

    return cls.from_dict(internal_map)
