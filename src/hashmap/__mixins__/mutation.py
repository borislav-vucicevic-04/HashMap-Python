from hashmap.__types__ import *
from hashmap.__types__ import Rule
from .interface import HashMapInterface

class Mutation[K, V](HashMapInterface[K, V]):
  def insert(self, key: K, value: V) -> None:
    self._assert_key_not_none(key)
    self._assert_value_not_none(value)

    if self.has(key):
      raise KeyError(f"The key already exists. \n\tSupplied key: {key}")

    self._map[key] = value

  def update(self, key: K, value: V) -> None:
    self._assert_key_not_none(key)
    self._assert_value_not_none(value)
    self._assert_key_exists(key)

    self._map[key] = value

  def update_with(self, key: K, value: V, handler: UpdateHandler[V]) -> None:
    self._assert_key_not_none(key)
    self._assert_value_not_none(value)
    self._assert_key_exists(key)

    old_value = self._map[key]
    new_value = handler(old_value, value)

    if new_value is None:
      raise ValueError("The callback must not return None.")

    self._map[key] = new_value

  def set(self, key: K, value: V) -> None:
    self._assert_key_not_none(key)
    self._assert_value_not_none(value)
    self._map[key] = value

  def set_with(self, key: K, value: V, handler: SetHandler[V]) -> None:
    self._assert_key_not_none(key)
    self._assert_value_not_none(value)

    old_value = self.get(key)
    new_value = handler(old_value, value)

    if new_value is None:
      raise ValueError("The callback must not return None.")

    self._map[key] = new_value

  def delete(self, key: K) -> None:
    self._assert_key_not_none(key)
    self._assert_key_exists(key)

    del self._map[key]

  def delete_first(self, rule: Rule[K, V], direction: Direction = "left") -> None:
    for key, value in self.get_entries(direction == 'right'):
      if rule(key, value):
        self.delete(key)
        return

    raise ValueError("No entry in the map matches the given rule.")

  def pop(self, key: K, default: V | None = None) -> V | None:
    self._assert_key_not_none(key)
    return self._map.pop(key, default)

  def pop_first(self, rule: Rule[K, V], direction: Direction = "left", default: tuple[K, V] | None = None) -> tuple[K, V] | None:
    for key, value in self.get_entries(direction == 'right'):
      if rule(key, value):
        self.delete(key)
        return (key, value)

    return default

  def sort(self, by: SortCriterion = "value", order: Order = "ascending") -> None:
    if by not in ('key', 'value'):
      raise ValueError("Argument 'by' must be either 'key' or 'value'")

    if order not in ('ascending', 'descending'):
      raise ValueError("Argument 'order' must be either 'ascending' or 'descending'")

    _by = 0 if by == 'key' else 1
    self._map = dict(sorted(self._map.items(), key=lambda item: item[_by], reverse=order=='descending')) # type: ignore