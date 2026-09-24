from collections.abc import ItemsView, KeysView, ValuesView
from ..__types__ import Rule

from .interface import HashMapInterface

class Lookup[K, V](HashMapInterface[K, V]):
  def get_keys(self) -> KeysView[K]:
    return self._map.keys()  

  def get_values(self) -> ValuesView[V]:
    return self._map.values()  

  def get_entries(self) -> ItemsView[K, V]:
    return self._map.items()  

  def size(self) -> int:
    return len(self._map)  

  def is_empty(self) -> bool:
    return self.size() == 0

  def count(self, rule: Rule[K, V]) -> int:
    return sum(1 for key, value in self.get_entries() if rule(key, value))

  def has(self, key: K) -> bool:
    self._assert_key_not_none(key)

    return key in self._map  

  def contains(self, value: V) -> bool:
    self._assert_value_not_none(value)

    return value in self._map.values()  

  def includes(self, key: K, value: V) -> bool:
    self._assert_key_not_none(key)
    self._assert_value_not_none(value)

    if not self.has(key): 
      return False

    return self._map[key] == value  

  def get(self, key: K, default: V | None = None) -> V | None:
    self._assert_key_not_none(key)

    return self._map.get(key, default)  

  def issuperset(self, other: HashMapInterface[K, V]) -> bool:
    for key, value in other.get_entries():
      if not self.includes(key, value):
        return False

    return True

  def issubset(self, other: HashMapInterface[K, V]) -> bool:
    return other.issuperset(self)