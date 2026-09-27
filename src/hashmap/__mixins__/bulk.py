from hashmap.__types__ import Handler, MergeHandler, ReplaceHandler, Rule
from .interface import HashMapInterface

class Bulk[K, V](HashMapInterface[K, V]):
  def add(self, other: HashMapInterface[K, V]) -> None:
    for key in other.get_keys():
      if self.has(key):
        raise KeyError(f"The key already exists. \n\tSupplied key {key}")

    for key, value in other.get_entries():
      self.insert(key, value)

  def replace(self, other: HashMapInterface[K, V]) -> None:
    for key in other.get_keys():
      if not self.has(key):
        raise KeyError(f"The key already doesn't exist. \n\tSupplied key {key}")

    for key, value in other.get_entries():
      self.update(key, value)

  def merge(self, other: HashMapInterface[K, V]) -> None:
    for key, value in other.get_entries():
      self.set(key, value)

  def clear(self) -> None:
    self._map.clear()

  def add_with[VO](self, other: HashMapInterface[K, VO], handler: Handler[K, VO, V]) -> None:
    entries: list[tuple[K, V]] = []

    for key, value in other.get_entries():
      result_value = handler(key, value)

      if self.has(key):
        raise KeyError(f"The key already exists. \n\tSupplied key: {key}")
      
      if result_value is None:
        raise ValueError("The callback must not return None")

      entries.append((key, result_value))

    for key, value in entries:
      self.insert(key, value)

  def replace_with[VO](self, other: HashMapInterface[K, VO], handler: ReplaceHandler[K, V, VO]) -> None:
    entries: list[tuple[K, V]] = []

    for key, value in other.get_entries():
      if not self.has(key):
        raise KeyError(f"The key doesn't exists. \n\tSupplied key: {key}")
      
      old_value = self.get(key)
      result_value = handler(key, old_value, value) # type: ignore

      
      if result_value is None:
        raise ValueError("The callback must not return None")

      entries.append((key, result_value))

    for key, value in entries:
      self.update(key, value)

  def merge_with[VO](self, other: HashMapInterface[K, VO], handler: MergeHandler[K, V, VO]) -> None:
    entries: list[tuple[K, V]] = []

    for key, value in other.get_entries():
      old_value = self.get(key)
      result_value = handler(key, old_value, value)

      if result_value is None:
        raise ValueError("The callback must not return None")
      else:
        entries.append((key, result_value))

    for key, value in entries:
      self.set(key, value)

  def delete_where(self, rule: Rule[K, V]) -> None:
    kept: dict[K, V] = {}

    for key, value in self.get_entries():
      if not rule(key, value):
        kept[key] = value

    self._map = kept

  def pop_where(self, rule: Rule[K, V]) -> HashMapInterface[K, V]:
    kept: dict[K, V] = {}
    popped: dict[K, V] = {}
    
    for key, value in self.get_entries():
      if rule(key, value):
        popped[key] = value
      else:
        kept[key] = value

    result = type(self)()
    result._map = popped
    self._map = kept

    return result