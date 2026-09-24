from abc import ABC, abstractmethod
from collections.abc import ItemsView, KeysView, ValuesView
from typing import Self
from ..__types__ import *

class HashMapInterface[K, V](ABC):
  def __init__(self) -> None:
    self.__map: dict[K, V] = {}

  # ==================================================
  # FACTORIES
  # ==================================================

  @classmethod
  @abstractmethod
  def from_entries(cls, entries: list[tuple[K, V]]) -> Self:
    """
    Create a new HashMap from a list of key-value pairs.

    Each tuple in ``entries`` represents a key-value pair that will be
    stored in the resulting HashMap. If the same key appears more than
    once, the value from its last occurrence is retained.

    All entries are deeply copied before being stored. As a result,
    subsequent mutations to mutable keys or values referenced by the
    original input do not affect the created HashMap.

    Args:
      entries: A list of key-value pairs used to initialize the HashMap.

    Returns:
      A new HashMap containing the provided entries.

    Raises:
      TypeError: If any key is not hashable.

    Examples:
      Create a HashMap from a list of entries:

      >>> hashmap = HashMap.from_entries([
      ...   ("name", "Alice"),
      ...   ("age", 30),
      ... ])
      >>> hashmap.get("name")
      'Alice'
      >>> hashmap.get("age")
      30

      If a key appears multiple times, the last value is retained:

      >>> hashmap = HashMap.from_entries([
      ...   ("a", 1),
      ...   ("a", 2),
      ... ])
      >>> hashmap.get("a")
      2

      Mutable values are deeply copied:

      >>> values = [1, 2, 3]
      >>> hashmap = HashMap.from_entries([
      ...   ("numbers", values),
      ... ])
      >>> values.append(4)
      >>> hashmap.get("numbers")
      [1, 2, 3]
    """
    ...

  @classmethod
  @abstractmethod
  def from_dict(cls, dictionary: dict[K, V]) -> Self:
    """
    Create a new HashMap from an existing dictionary.

    The supplied dictionary and all supported nested objects are deeply
    copied into the new HashMap. Subsequent mutations to the original
    dictionary or to mutable objects contained within it do not affect
    the created HashMap.

    Args:
      dictionary: The dictionary used to initialize the HashMap.

    Returns:
      A new HashMap containing a deep copy of the supplied dictionary.

    Examples:
      Create a HashMap from a dictionary:

      >>> hashmap = HashMap.from_dict({
      ...   "name": "Alice",
      ...   "age": 30,
      ... })
      >>> hashmap.get("name")
      'Alice'
      >>> hashmap.get("age")
      30

      Changes to the original dictionary do not affect the HashMap:

      >>> source = {"a": 1}
      >>> hashmap = HashMap.from_dict(source)
      >>> source["a"] = 100
      >>> hashmap.get("a")
      1

      Nested mutable values are also deeply copied:

      >>> source = {
      ...   "numbers": [1, 2, 3],
      ... }
      >>> hashmap = HashMap.from_dict(source)
      >>> source["numbers"].append(4)
      >>> hashmap.get("numbers")
      [1, 2, 3]
    """
    ...

  # ==================================================
  # LOOKUP
  # ==================================================

  @abstractmethod
  def get_keys(self) -> KeysView[K]:
    """
    Return a dynamic view of the keys stored in the HashMap.

    The returned view reflects changes made to the HashMap after the view
    has been created. Keys are exposed in the current iteration order of
    the HashMap.

    The returned object does not contain copies of the keys.

    Returns:
      A dynamic view containing the keys stored in the HashMap.

    Examples:
      Retrieve the keys of a HashMap:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> keys = hashmap.get_keys()
      >>> list(keys)
      ['a', 'b']

      The view reflects subsequent changes to the HashMap:

      >>> hashmap.insert("c", 3)
      >>> list(keys)
      ['a', 'b', 'c']
    """
    ...

  @abstractmethod
  def get_values(self) -> ValuesView[V]:
    """
    Return a dynamic view of the values stored in the HashMap.

    The returned view reflects changes made to the HashMap after the view
    has been created. Values are exposed in the current iteration order of
    the HashMap.

    Stored values are returned by reference and are not deeply copied.
    Mutable objects accessed through the view therefore refer to the same
    objects stored in the HashMap.

    Returns:
      A dynamic view containing the values stored in the HashMap.

    Examples:
      Retrieve the values of a HashMap:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> values = hashmap.get_values()
      >>> list(values)
      [1, 2]

      The view reflects subsequent changes to the HashMap:

      >>> hashmap.update("a", 10)
      >>> list(values)
      [10, 2]

      Mutable values are exposed by reference:

      >>> hashmap = HashMap.from_dict({
      ...   "items": [1, 2],
      ... })
      >>> values = hashmap.get_values()
      >>> next(iter(values)).append(3)
      >>> hashmap.get("items")
      [1, 2, 3]
    """
    ...

  @abstractmethod
  def get_entries(self) -> ItemsView[K, V]:
    """
    Return a dynamic view of the entries stored in the HashMap.

    Each entry is exposed as a ``(key, value)`` tuple. Entries are
    returned in the current iteration order of the HashMap.

    The returned view reflects changes made to the HashMap after the view
    has been created.

    Keys and values contained in the entries are not deeply copied.
    Mutable values therefore refer to the same objects stored in the
    HashMap.

    Returns:
      A dynamic view containing the HashMap's key-value pairs.

    Examples:
      Retrieve the entries of a HashMap:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> entries = hashmap.get_entries()
      >>> list(entries)
      [('a', 1), ('b', 2)]

      The view reflects subsequent changes to the HashMap:

      >>> hashmap.insert("c", 3)
      >>> list(entries)
      [('a', 1), ('b', 2), ('c', 3)]

      Mutable values are exposed by reference:

      >>> hashmap = HashMap.from_dict({
      ...   "items": [1, 2],
      ... })
      >>> entries = hashmap.get_entries()
      >>> key, value = next(iter(entries))
      >>> value.append(3)
      >>> hashmap.get("items")
      [1, 2, 3]
    """
    ...

  @abstractmethod
  def size(self) -> int:
    """
    Return the number of entries stored in the HashMap.

    Returns:
      The number of key-value pairs currently stored in the HashMap.

    Examples:
      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 3,
      ... })
      >>> hashmap.size()
      3

      An empty HashMap has a size of zero:

      >>> hashmap = HashMap.from_dict({})
      >>> hashmap.size()
      0
    """
    ...

  @abstractmethod
  def is_empty(self) -> bool:
    """
    Check whether the HashMap contains no entries.

    Returns:
      ``True`` if the HashMap contains no entries, otherwise ``False``.

    Examples:
      Check an empty HashMap:

      >>> hashmap = HashMap.from_dict({})
      >>> hashmap.is_empty()
      True

      Check a HashMap that contains entries:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ... })
      >>> hashmap.is_empty()
      False
    """
    ...

  @abstractmethod
  def count(self, rule: Rule[K, V]) -> int:
    """
    Count the entries that satisfy a given rule.

    The rule is called once for each entry as ``rule(key, value)`` and
    must return a boolean value. Entries are evaluated in the HashMap's
    current iteration order.

    Exceptions raised by the rule are propagated to the caller.

    Args:
      rule: A callable that receives a key and its associated value and
        returns ``True`` when the entry should be counted.

    Returns:
      The number of entries for which ``rule`` returns ``True``.

    Examples:
      Count entries whose values are greater than 10:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 5,
      ...   "b": 20,
      ...   "c": 15,
      ... })
      >>> hashmap.count(lambda key, value: value > 10)
      2

      The rule may inspect both the key and the value:

      >>> hashmap.count(
      ...   lambda key, value: key != "b" and value >= 5
      ... )
      2
    """
    ...

  @abstractmethod
  def has(self, key: K) -> bool:
    """
    Check whether the HashMap contains a given key.

    Args:
      key: The key whose presence should be checked.

    Returns:
      ``True`` if the key exists in the HashMap, otherwise ``False``.

    Examples:
      >>> hashmap = HashMap.from_dict({
      ...   "name": "Alice",
      ...   "age": 30,
      ... })
      >>> hashmap.has("name")
      True
      >>> hashmap.has("email")
      False
    """
    ...

  @abstractmethod
  def contains(self, value: V) -> bool:
    """
    Check whether the HashMap contains a given value.

    Stored values are compared to ``value`` using the equality operator
    ``==``. Values used with this method must therefore support equality
    comparison.

    Args:
      value: The value whose presence should be checked.

    Returns:
      ``True`` if at least one stored entry has a value equal to
      ``value``, otherwise ``False``.

    Examples:
      >>> hashmap = HashMap.from_dict({
      ...   "a": 10,
      ...   "b": 20,
      ... })
      >>> hashmap.contains(20)
      True
      >>> hashmap.contains(30)
      False
    """
    ...

  @abstractmethod
  def includes(self, key: K, value: V) -> bool:
    """
    Check whether the HashMap contains a specific key-value pair.

    The method returns ``True`` only when ``key`` exists and its
    associated value compares equal to ``value`` using ``==``. Stored
    values used with this method must support equality comparison.

    Args:
      key: The key to look up.
      value: The value expected to be associated with the key.

    Returns:
      ``True`` if the specified key-value pair exists, otherwise
      ``False``.

    Examples:
      >>> hashmap = HashMap.from_dict({
      ...   "a": 10,
      ...   "b": 20,
      ... })
      >>> hashmap.includes("a", 10)
      True
      >>> hashmap.includes("a", 20)
      False
      >>> hashmap.includes("c", 10)
      False
    """
    ...

  @abstractmethod
  def issuperset(
    self,
    other: HashMapInterface[K, V],
  ) -> bool:
    """
    Check whether this HashMap contains every entry from another HashMap.

    An entry is considered present only when the same key exists in this
    HashMap and its associated value compares equal using ``==``. Stored
    values involved in the comparison must support equality comparison.

    Args:
      other: The HashMap whose entries should be checked against this
        instance.

    Returns:
      ``True`` if every key-value pair in ``other`` is also present in
      this HashMap, otherwise ``False``.

    Examples:
      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 3,
      ... })
      >>> other = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> hashmap.issuperset(other)
      True

      A matching key with a different value does not satisfy the check:

      >>> other = HashMap.from_dict({
      ...   "a": 100,
      ... })
      >>> hashmap.issuperset(other)
      False
    """
    ...

  @abstractmethod
  def issubset(
    self,
    other: HashMapInterface[K, V],
  ) -> bool:
    """
    Check whether every entry in this HashMap exists in another HashMap.

    An entry is considered present only when the same key exists in
    ``other`` and its associated value compares equal using ``==``.
    Stored values involved in the comparison must support equality
    comparison.

    Args:
      other: The HashMap against which this instance should be checked.

    Returns:
      ``True`` if every key-value pair in this HashMap is also present in
      ``other``, otherwise ``False``.

    Examples:
      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> other = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 3,
      ... })
      >>> hashmap.issubset(other)
      True

      A matching key with a different value does not satisfy the check:

      >>> other = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 100,
      ... })
      >>> hashmap.issubset(other)
      False
    """
    ...

  @abstractmethod
  def get(self, key: K, default: V | None = None) -> V | None:
    """
    Return the value associated with a given key.

    If the key exists, the stored value is returned directly. Mutable
    values are therefore returned by reference rather than being copied.

    If the key does not exist, ``default`` is returned without modifying
    the HashMap. The supplied default value is returned directly and is
    not stored in the HashMap.

    Args:
      key: The key whose associated value should be returned.
      default: The value returned when ``key`` does not exist. Defaults
        to ``None``.

    Returns:
      The value associated with ``key`` if it exists, otherwise
      ``default``.

    Examples:
      Retrieve an existing value:

      >>> hashmap = HashMap.from_dict({
      ...   "name": "Alice",
      ...   "age": 30,
      ... })
      >>> hashmap.get("name")
      'Alice'

      A missing key returns ``None`` by default:

      >>> hashmap.get("email") is None
      True

      A custom default may be supplied:

      >>> hashmap.get("email", "unknown")
      'unknown'

      Retrieving a mutable value returns the stored object:

      >>> hashmap = HashMap.from_dict({
      ...   "numbers": [1, 2, 3],
      ... })
      >>> numbers = hashmap.get("numbers")
      >>> numbers.append(4)
      >>> hashmap.get("numbers")
      [1, 2, 3, 4]
    """
    ...

  # ==================================================
  # MUTATION
  # ==================================================

  @abstractmethod
  def insert(self, key: K, value: V) -> None:
    """
    Insert a new key-value pair into the HashMap.

    The key must not already exist in the HashMap. Both the key and value
    are stored directly without being deeply copied. Mutable values
    therefore remain shared with the caller.

    Args:
      key: The key to insert.
      value: The value to associate with the key.

    Raises:
      KeyError: If the key already exists.
      TypeError: If the key is not hashable.

    Examples:
      Insert a new entry:

      >>> hashmap = HashMap.from_dict({})
      >>> hashmap.insert("name", "Alice")
      >>> hashmap.get("name")
      'Alice'

      Inserting an existing key raises ``KeyError``:

      >>> hashmap.insert("name", "Bob")
      Traceback (most recent call last):
      ...
      KeyError: ...

      Values are stored directly rather than deeply copied:

      >>> numbers = [1, 2, 3]
      >>> hashmap.insert("numbers", numbers)
      >>> numbers.append(4)
      >>> hashmap.get("numbers")
      [1, 2, 3, 4]
    """
    ...

  @abstractmethod
  def update(self, key: K, value: V) -> None:
    """
    Replace the value associated with an existing key.

    The key must already exist in the HashMap. The supplied value is
    stored directly without being deeply copied.

    Args:
      key: The key whose associated value should be replaced.
      value: The new value to associate with the key.

    Raises:
      KeyError: If the key does not exist.

    Examples:
      Update an existing entry:

      >>> hashmap = HashMap.from_dict({
      ...   "name": "Alice",
      ...   "age": 30,
      ... })
      >>> hashmap.update("age", 31)
      >>> hashmap.get("age")
      31

      Updating a missing key raises ``KeyError``:

      >>> hashmap.update("email", "alice@example.com")
      Traceback (most recent call last):
      ...
      KeyError: ...
    """
    ...

  @abstractmethod
  def update_with(
    self,
    key: K,
    value: V,
    handler: UpdateHandler[V],
  ) -> None:
    """
    Update an existing value using a callback.

    The handler receives the currently stored value followed by the new
    value supplied to this method. Its return value becomes the value
    associated with the key.

    The handler is called as ``handler(old_value, new_value)``.

    The key must already exist in the HashMap. Exceptions raised by the
    handler are propagated to the caller.

    Args:
      key: The key whose associated value should be updated.
      value: The new value supplied to the handler.
      handler: A callable that receives the current value and the supplied
        new value and returns the value that should be stored.

    Raises:
      KeyError: If the key does not exist.

    Examples:
      Update a value using both its current and supplied values:

      >>> hashmap = HashMap.from_dict({
      ...   "score": 10,
      ... })
      >>> hashmap.update_with(
      ...   "score",
      ...   5,
      ...   lambda old_value, new_value: old_value + new_value,
      ... )
      >>> hashmap.get("score")
      15

      The handler may completely replace the existing value:

      >>> hashmap.update_with(
      ...   "score",
      ...   100,
      ...   lambda old_value, new_value: new_value,
      ... )
      >>> hashmap.get("score")
      100
    """
    ...

  @abstractmethod
  def set(self, key: K, value: V) -> None:
    """
    Associate a value with a key.

    If the key already exists, its current value is replaced. If the key
    does not exist, a new entry is inserted.

    The supplied value is stored directly without being deeply copied.

    Args:
      key: The key to associate with the value.
      value: The value to store.

    Raises:
      TypeError: If a newly inserted key is not hashable.

    Examples:
      Insert an entry when the key does not exist:

      >>> hashmap = HashMap.from_dict({})
      >>> hashmap.set("name", "Alice")
      >>> hashmap.get("name")
      'Alice'

      Replace the value when the key already exists:

      >>> hashmap.set("name", "Bob")
      >>> hashmap.get("name")
      'Bob'
    """
    ...

  @abstractmethod
  def set_with(
    self,
    key: K,
    value: V,
    handler: SetHandler[V],
  ) -> None:
    """
    Set a value using a callback.

    The handler receives the currently stored value followed by the new
    value supplied to this method. If the key does not exist, the old
    value passed to the handler is ``None``.

    The handler is called as ``handler(old_value, new_value)`` and its
    return value becomes the value associated with the key.

    Exceptions raised by the handler are propagated to the caller.

    Args:
      key: The key whose value should be set.
      value: The new value supplied to the handler.
      handler: A callable that receives the existing value, or ``None``
        when the key is absent, followed by the supplied new value.

    Raises:
      TypeError: If a newly inserted key is not hashable.

    Examples:
      Update an existing value:

      >>> hashmap = HashMap.from_dict({
      ...   "count": 10,
      ... })
      >>> hashmap.set_with(
      ...   "count",
      ...   5,
      ...   lambda old_value, new_value: old_value + new_value,
      ... )
      >>> hashmap.get("count")
      15

      The handler receives ``None`` when the key does not exist:

      >>> hashmap.set_with(
      ...   "missing",
      ...   5,
      ...   lambda old_value, new_value:
      ...     new_value if old_value is None else old_value + new_value,
      ... )
      >>> hashmap.get("missing")
      5
    """
    ...

  @abstractmethod
  def delete(self, key: K) -> None:
    """
    Remove an entry from the HashMap.

    Args:
      key: The key of the entry to remove.

    Raises:
      KeyError: If the key does not exist.

    Examples:
      Delete an existing entry:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> hashmap.delete("a")
      >>> hashmap.has("a")
      False

      Deleting a missing key raises ``KeyError``:

      >>> hashmap.delete("missing")
      Traceback (most recent call last):
      ...
      KeyError: ...
    """
    ...

  @abstractmethod
  def delete_first(
    self,
    rule: Rule[K, V],
    direction: Direction = "left",
  ) -> None:
    """
    Delete the first entry that satisfies a given rule.

    The rule is called as ``rule(key, value)``. Entries are inspected
    according to ``direction``. A direction of ``"left"`` searches from
    the beginning of the current iteration order, while ``"right"``
    searches from the end.

    Only the first matching entry is removed.

    Exceptions raised by the rule are propagated to the caller.

    Args:
      rule: A callable that receives a key and its associated value and
        returns ``True`` when the entry matches.
      direction: The direction from which the search begins. Must be
        ``"left"`` or ``"right"``. Defaults to ``"left"``.

    Raises:
      ValueError: If no entry satisfies the rule.

    Examples:
      Delete the first matching entry from the left:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 2,
      ... })
      >>> hashmap.delete_first(
      ...   lambda key, value: value == 2
      ... )
      >>> hashmap.has("b")
      False
      >>> hashmap.has("c")
      True

      Search from the right instead:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 2,
      ... })
      >>> hashmap.delete_first(
      ...   lambda key, value: value == 2,
      ...   direction="right",
      ... )
      >>> hashmap.has("b")
      True
      >>> hashmap.has("c")
      False
    """
    ...

  @abstractmethod
  def pop(
    self,
    key: K,
    default: V | None = None,
  ) -> V | None:
    """
    Remove an entry and return its associated value.

    If the key exists, the entry is removed and its stored value is
    returned directly without being copied.

    If the key does not exist, ``default`` is returned and the HashMap
    remains unchanged. The default value is not inserted into the
    HashMap.

    Args:
      key: The key of the entry to remove.
      default: The value returned when the key does not exist. Defaults
        to ``None``.

    Returns:
      The value associated with the removed key, or ``default`` if the
      key does not exist.

    Examples:
      Remove and return an existing value:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> hashmap.pop("a")
      1
      >>> hashmap.has("a")
      False

      Return ``None`` when the key does not exist:

      >>> hashmap.pop("missing") is None
      True

      A custom default may be supplied:

      >>> hashmap.pop("missing", 100)
      100
    """
    ...

  @abstractmethod
  def pop_first(
    self,
    rule: Rule[K, V],
    direction: Direction = "left",
  ) -> tuple[K, V] | None:
    """
    Remove and return the first entry that satisfies a given rule.

    The rule is called as ``rule(key, value)``. Entries are inspected
    according to ``direction``. A direction of ``"left"`` searches from
    the beginning of the current iteration order, while ``"right"``
    searches from the end.

    If a matching entry is found, it is removed and returned as a
    ``(key, value)`` tuple. If no entry matches, ``None`` is returned.

    Exceptions raised by the rule are propagated to the caller.

    Args:
      rule: A callable that receives a key and its associated value and
        returns ``True`` when the entry matches.
      direction: The direction from which the search begins. Must be
        ``"left"`` or ``"right"``. Defaults to ``"left"``.

    Returns:
      The first matching key-value pair as a ``(key, value)`` tuple, or
      ``None`` if no entry satisfies the rule.

    Examples:
      Remove the first matching entry from the left:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 2,
      ... })
      >>> hashmap.pop_first(
      ...   lambda key, value: value == 2
      ... )
      ('b', 2)
      >>> hashmap.has("b")
      False

      Search from the right:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 2,
      ... })
      >>> hashmap.pop_first(
      ...   lambda key, value: value == 2,
      ...   direction="right",
      ... )
      ('c', 2)

      ``None`` is returned when no entry matches:

      >>> hashmap.pop_first(
      ...   lambda key, value: value > 100
      ... ) is None
      True
    """
    ...

  @abstractmethod
  def sort(
    self,
    by: SortCriterion = "value",
    order: Order = "ascending",
  ) -> None:
    """
    Sort the entries of the HashMap in place.

    Sorting changes the iteration order of the internal mapping without
    changing any keys or values.

    Entries may be sorted by either their keys or their values. The
    resulting order may be ascending or descending.

    Objects used as the selected sorting criterion must support ordering
    with one another. If they cannot be ordered, the resulting
    ``TypeError`` is propagated to the caller.

    Sorting is stable. Entries whose selected sorting values compare
    equally retain their existing relative order.

    Args:
      by: The component used for sorting. Must be ``"key"`` or
        ``"value"``. Defaults to ``"value"``.
      order: The sorting order. Must be ``"ascending"`` or
        ``"descending"``. Defaults to ``"ascending"``.

    Raises:
      TypeError: If the selected keys or values cannot be ordered with
        one another.

    Examples:
      Sort entries by value in ascending order:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 30,
      ...   "b": 10,
      ...   "c": 20,
      ... })
      >>> hashmap.sort()
      >>> hashmap.foreach(print)
      ...

      Sort entries by key in descending order:

      >>> hashmap.sort(
      ...   by="key",
      ...   order="descending",
      ... )
    """
    ...

  # ==================================================
  # BULK MUTATION
  # ==================================================

  @abstractmethod
  def add(self, other: HashMapInterface[K, V]) -> None:
    """
    Insert all entries from another HashMap.

    Every key from ``other`` must be absent from the current HashMap.
    If any key already exists, the operation fails and no entries are
    inserted.

    Inserted keys and values follow the same storage behavior as
    ``insert`` and are not deeply copied.

    Args:
      other: The HashMap whose entries should be inserted.

    Raises:
      KeyError: If any key from ``other`` already exists in the current
        HashMap.
      TypeError: If any inserted key is not hashable.

    Examples:
      Insert all entries from another HashMap:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ... })
      >>> other = HashMap.from_dict({
      ...   "b": 2,
      ...   "c": 3,
      ... })
      >>> hashmap.add(other)
      >>> hashmap.get("b")
      2
      >>> hashmap.get("c")
      3

      The operation fails if any key already exists:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ... })
      >>> other = HashMap.from_dict({
      ...   "b": 2,
      ...   "a": 3,
      ... })
      >>> hashmap.add(other)
      Traceback (most recent call last):
      ...
      KeyError: ...

      No entries are inserted when the operation fails:

      >>> hashmap.has("b")
      False
    """
    ...

  @abstractmethod
  def replace(self, other: HashMapInterface[K, V]) -> None:
    """
    Replace existing values using entries from another HashMap.

    Every key from ``other`` must already exist in the current HashMap.
    If any key is missing, the operation fails and no values are
    replaced.

    Replacement values follow the same storage behavior as ``update``
    and are not deeply copied.

    Args:
      other: The HashMap containing replacement values.

    Raises:
      KeyError: If any key from ``other`` does not exist in the current
        HashMap.

    Examples:
      Replace multiple existing values:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> other = HashMap.from_dict({
      ...   "a": 10,
      ...   "b": 20,
      ... })
      >>> hashmap.replace(other)
      >>> hashmap.get("a")
      10
      >>> hashmap.get("b")
      20

      The operation fails if any key is missing:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ... })
      >>> other = HashMap.from_dict({
      ...   "a": 10,
      ...   "b": 20,
      ... })
      >>> hashmap.replace(other)
      Traceback (most recent call last):
      ...
      KeyError: ...

      No existing values are changed when the operation fails:

      >>> hashmap.get("a")
      1
    """
    ...

  @abstractmethod
  def merge(self, other: HashMapInterface[K, V]) -> None:
    """
    Merge all entries from another HashMap into the current HashMap.

    Entries are processed in the iteration order of ``other``. If a key
    already exists, its current value is replaced. If a key does not
    exist, a new entry is inserted.

    Keys and values follow the same storage behavior as ``set`` and are
    not deeply copied.

    Args:
      other: The HashMap whose entries should be merged into the current
        instance.

    Raises:
      TypeError: If a newly inserted key is not hashable.

    Examples:
      Merge new and existing entries:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> other = HashMap.from_dict({
      ...   "b": 20,
      ...   "c": 30,
      ... })
      >>> hashmap.merge(other)
      >>> hashmap.get("a")
      1
      >>> hashmap.get("b")
      20
      >>> hashmap.get("c")
      30
    """
    ...

  @abstractmethod
  def clear(self) -> None:
    """
    Remove all entries from the HashMap.

    The current HashMap instance is retained and becomes empty.

    Examples:
      Remove all entries:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> hashmap.clear()
      >>> hashmap.size()
      0
    """
    ...

  @abstractmethod
  def add_with[VO](
    self,
    other: HashMapInterface[K, VO],
    handler: Handler[K, VO, V],
  ) -> None:
    """
    Insert transformed entries from another HashMap.

    For every entry in ``other``, the handler is called as
    ``handler(key, other_value)``. The returned value is associated with
    the same key in the current HashMap.

    Every key from ``other`` must be absent from the current HashMap.
    If any key already exists, the operation fails and no entries are
    inserted.

    Exceptions raised by the handler are propagated to the caller.

    Args:
      other: The HashMap containing the entries to transform and insert.
      handler: A callable that receives a key and its value from
        ``other`` and returns the value to store in the current HashMap.

    Raises:
      KeyError: If any key from ``other`` already exists in the current
        HashMap.
      TypeError: If any inserted key is not hashable.

    Examples:
      Transform values while inserting entries:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ... })
      >>> other = HashMap.from_dict({
      ...   "b": "10",
      ...   "c": "20",
      ... })
      >>> hashmap.add_with(
      ...   other,
      ...   lambda key, value: int(value),
      ... )
      >>> hashmap.get("b")
      10
      >>> hashmap.get("c")
      20

      The key may also be used by the handler:

      >>> hashmap = HashMap.from_dict({})
      >>> other = HashMap.from_dict({
      ...   "a": 10,
      ...   "b": 20,
      ... })
      >>> hashmap.add_with(
      ...   other,
      ...   lambda key, value: f"{key}:{value}",
      ... )
      >>> hashmap.get("a")
      'a:10'
    """
    ...

  @abstractmethod
  def replace_with[VO](
    self,
    other: HashMapInterface[K, VO],
    handler: ReplaceHandler[K, VO, V],
  ) -> None:
    """
    Replace existing values using transformed values from another
    HashMap.

    For every entry in ``other``, the handler is called as
    ``handler(key, old_value, other_value)``.

    ``old_value`` is the value currently stored in this HashMap and
    ``other_value`` is the value associated with the same key in
    ``other``. The value returned by the handler becomes the new stored
    value.

    Every key from ``other`` must already exist in the current HashMap.
    If any key is missing, the operation fails and no values are
    replaced.

    Exceptions raised by the handler are propagated to the caller.

    Args:
      other: The HashMap containing values used to produce replacements.
      handler: A callable that receives the key, the currently stored
        value, and the corresponding value from ``other``.

    Raises:
      KeyError: If any key from ``other`` does not exist in the current
        HashMap.

    Examples:
      Combine current and incoming values:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 10,
      ...   "b": 20,
      ... })
      >>> other = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> hashmap.replace_with(
      ...   other,
      ...   lambda key, old_value, other_value:
      ...     old_value + other_value,
      ... )
      >>> hashmap.get("a")
      11
      >>> hashmap.get("b")
      22

      The key may participate in the transformation:

      >>> hashmap.replace_with(
      ...   HashMap.from_dict({
      ...     "a": 5,
      ...     "b": 5,
      ...   }),
      ...   lambda key, old_value, other_value:
      ...     old_value + other_value if key == "a" else old_value,
      ... )
      >>> hashmap.get("a")
      16
    """
    ...

  @abstractmethod
  def merge_with[VO](
    self,
    other: HashMapInterface[K, VO],
    handler: MergeHandler[K, VO, V],
  ) -> None:
    """
    Merge transformed entries from another HashMap.

    Entries are processed in the iteration order of ``other``. For each
    entry, the handler is called as
    ``handler(key, old_value, other_value)``.

    ``old_value`` is the value currently stored in this HashMap, or
    ``None`` if the key does not yet exist. ``other_value`` is the value
    associated with the key in ``other``.

    The value returned by the handler is stored under the corresponding
    key. Existing entries are replaced and missing entries are inserted.

    Exceptions raised by the handler are propagated to the caller.

    Args:
      other: The HashMap containing values used during the merge.
      handler: A callable that receives the key, the existing value or
        ``None``, and the corresponding value from ``other``.

    Raises:
      TypeError: If a newly inserted key is not hashable.

    Examples:
      Merge values using existing values when available:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 10,
      ... })
      >>> other = HashMap.from_dict({
      ...   "a": 5,
      ...   "b": 20,
      ... })
      >>> hashmap.merge_with(
      ...   other,
      ...   lambda key, old_value, other_value:
      ...     other_value
      ...     if old_value is None
      ...     else old_value + other_value,
      ... )
      >>> hashmap.get("a")
      15
      >>> hashmap.get("b")
      20
    """
    ...

  @abstractmethod
  def delete_where(self, rule: Rule[K, V]) -> None:
    """
    Delete all entries that satisfy a given rule.

    The rule is called as ``rule(key, value)`` for entries in the current
    iteration order. Every entry for which the rule returns ``True`` is
    removed.

    If no entries satisfy the rule, the HashMap remains unchanged.

    Exceptions raised by the rule are propagated to the caller.

    Args:
      rule: A callable that receives a key and its associated value and
        returns ``True`` when the entry should be removed.

    Examples:
      Delete all entries whose values are even:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 3,
      ...   "d": 4,
      ... })
      >>> hashmap.delete_where(
      ...   lambda key, value: value % 2 == 0
      ... )
      >>> hashmap.has("a")
      True
      >>> hashmap.has("b")
      False
      >>> hashmap.has("c")
      True
      >>> hashmap.has("d")
      False

      No error is raised when nothing matches:

      >>> hashmap.delete_where(
      ...   lambda key, value: value > 100
      ... )
    """
    ...

  @abstractmethod
  def pop_where(
    self,
    rule: Rule[K, V],
  ) -> HashMapInterface[K, V]:
    """
    Remove and return all entries that satisfy a given rule.

    The rule is called as ``rule(key, value)`` for entries in the current
    iteration order. Every matching entry is removed from the current
    HashMap and placed into a new HashMap.

    The returned HashMap preserves the relative iteration order of the
    removed entries.

    Removed keys and values are transferred using the same reference
    behavior as ``pop`` and are not deeply copied.

    If no entries satisfy the rule, an empty HashMap is returned.

    Exceptions raised by the rule are propagated to the caller.

    Args:
      rule: A callable that receives a key and its associated value and
        returns ``True`` when the entry should be removed.

    Returns:
      A new HashMap containing all removed entries.

    Examples:
      Remove and return all matching entries:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 3,
      ...   "d": 4,
      ... })
      >>> removed = hashmap.pop_where(
      ...   lambda key, value: value % 2 == 0
      ... )
      >>> removed.get("b")
      2
      >>> removed.get("d")
      4
      >>> hashmap.has("b")
      False
      >>> hashmap.has("d")
      False

      An empty HashMap is returned when nothing matches:

      >>> removed = hashmap.pop_where(
      ...   lambda key, value: value > 100
      ... )
      >>> removed.size()
      0
    """
    ...

  # ==================================================
  # TRANSFORMATION
  # ==================================================

  @abstractmethod
  def deepcopy(self) -> HashMapInterface[K, V]:
    """
    Create a deep copy of the HashMap.

    The returned HashMap is fully independent from the current instance.
    Its internal mapping, keys, values, and supported nested objects are
    deeply copied.

    Mutating mutable objects contained in either HashMap does not affect
    the other.

    Returns:
      A deeply copied HashMap containing the same entries and iteration
      order as the current instance.

    Examples:
      Create an independent copy:

      >>> hashmap = HashMap.from_dict({
      ...   "numbers": [1, 2, 3],
      ... })
      >>> copied = hashmap.deepcopy()
      >>> copied.get("numbers").append(4)
      >>> hashmap.get("numbers")
      [1, 2, 3]
      >>> copied.get("numbers")
      [1, 2, 3, 4]
    """
    ...


  @abstractmethod
  def foreach(self, callback: Callback[K, V]) -> None:
    """
    Execute a callback for every entry in the HashMap.

    Entries are visited in the current iteration order. The callback is
    invoked as ``callback(key, value)``.

    Keys and values are passed directly to the callback and are not
    copied. As a result, the callback may mutate mutable objects stored
    as values.

    Exceptions raised by the callback are propagated to the caller.

    Args:
      callback: A callable that receives each key and its associated
        value.

    Examples:
      Execute an operation for every entry:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> hashmap.foreach(
      ...   lambda key, value: print(key, value)
      ... )
      a 1
      b 2

      Mutable stored values may be modified by the callback:

      >>> hashmap = HashMap.from_dict({
      ...   "a": [1],
      ...   "b": [2],
      ... })
      >>> hashmap.foreach(
      ...   lambda key, value: value.append(10)
      ... )
      >>> hashmap.get("a")
      [1, 10]
    """
    ...


  @abstractmethod
  def map[RK, RV](
    self,
    handler: Handler[K, V, tuple[RK, RV]],
  ) -> HashMapInterface[RK, RV]:
    """
    Transform every entry and return the results in a new HashMap.

    Entries are processed in the current iteration order. The handler is
    called as ``handler(key, value)`` and must return a ``(key, value)``
    tuple representing the transformed entry.

    Handler results are inserted directly into the resulting HashMap and
    are not deeply copied. The handler is expected to produce appropriate
    transformed objects rather than return mutable references that should
    remain independent from the original HashMap.

    Every produced key must be unique within the resulting HashMap. If a
    handler produces a key that has already been produced for an earlier
    entry, ``KeyError`` is raised.

    Exceptions raised by the handler are propagated to the caller.

    Args:
      handler: A callable that receives each key and value and returns a
        transformed key-value pair.

    Returns:
      A new HashMap containing the transformed entries.

    Raises:
      KeyError: If multiple transformed entries produce the same key.
      TypeError: If a transformed key is not hashable.

    Examples:
      Transform both keys and values:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ... })
      >>> mapped = hashmap.map(
      ...   lambda key, value: (key.upper(), value * 10)
      ... )
      >>> mapped.get("A")
      10
      >>> mapped.get("B")
      20

      Producing the same key more than once raises ``KeyError``:

      >>> hashmap.map(
      ...   lambda key, value: ("same", value)
      ... )
      Traceback (most recent call last):
      ...
      KeyError: ...
    """
    ...


  @abstractmethod
  def filter(
    self,
    rule: Rule[K, V],
    deepcopy: bool = False,
  ) -> HashMapInterface[K, V]:
    """
    Return a new HashMap containing entries that satisfy a given rule.

    The rule is called as ``rule(key, value)`` for entries in the current
    iteration order. Entries for which the rule returns ``True`` are
    included in the resulting HashMap while preserving their relative
    order.

    By default, matching keys and values are transferred by reference.
    When ``deepcopy`` is ``True``, matching entries are deeply copied so
    that mutable objects in the resulting HashMap are independent from
    those in the original.

    Exceptions raised by the rule are propagated to the caller.

    Args:
      rule: A callable that receives a key and its associated value and
        returns ``True`` when the entry should be included.
      deepcopy: Whether matching entries should be deeply copied.
        Defaults to ``False``.

    Returns:
      A new HashMap containing all matching entries.

    Examples:
      Filter entries by value:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 3,
      ... })
      >>> filtered = hashmap.filter(
      ...   lambda key, value: value >= 2
      ... )
      >>> filtered.has("a")
      False
      >>> filtered.has("b")
      True
      >>> filtered.has("c")
      True

      By default, mutable values remain shared:

      >>> hashmap = HashMap.from_dict({
      ...   "items": [1, 2],
      ... })
      >>> filtered = hashmap.filter(
      ...   lambda key, value: True
      ... )
      >>> filtered.get("items").append(3)
      >>> hashmap.get("items")
      [1, 2, 3]

      Deep copying creates independent values:

      >>> hashmap = HashMap.from_dict({
      ...   "items": [1, 2],
      ... })
      >>> filtered = hashmap.filter(
      ...   lambda key, value: True,
      ...   deepcopy=True,
      ... )
      >>> filtered.get("items").append(3)
      >>> hashmap.get("items")
      [1, 2]
    """
    ...


  @abstractmethod
  def map_then_filter[RK, RV](
    self,
    handler: Handler[K, V, tuple[RK, RV]],
    rule: Rule[RK, RV],
  ) -> HashMapInterface[RK, RV]:
    """
    Transform all entries and then filter the transformed results.

    Entries are first processed by ``handler``, which is called as
    ``handler(key, value)`` and must return a transformed ``(key, value)``
    pair.

    The resulting entries are then evaluated by ``rule``, which receives
    the transformed key and value as ``rule(key, value)``.

    Entries are processed in the current iteration order. Transformed
    objects are stored directly and are not deeply copied.

    Every transformed key must be unique. If multiple source entries
    produce the same key, ``KeyError`` is raised.

    Exceptions raised by either callback are propagated to the caller.

    Args:
      handler: A callable that transforms each original entry into a new
        key-value pair.
      rule: A callable that receives a transformed key and value and
        returns ``True`` when the entry should be retained.

    Returns:
      A new HashMap containing transformed entries that satisfy the rule.

    Raises:
      KeyError: If multiple transformed entries produce the same key.
      TypeError: If a transformed key is not hashable.

    Examples:
      Transform entries before filtering them:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 3,
      ... })
      >>> result = hashmap.map_then_filter(
      ...   lambda key, value: (key.upper(), value * 10),
      ...   lambda key, value: value >= 20,
      ... )
      >>> result.has("A")
      False
      >>> result.get("B")
      20
      >>> result.get("C")
      30
    """
    ...


  @abstractmethod
  def filter_then_map[RK, RV](
    self,
    rule: Rule[K, V],
    handler: Handler[K, V, tuple[RK, RV]],
  ) -> HashMapInterface[RK, RV]:
    """
    Filter the entries and then transform the matching results.

    The rule is evaluated first as ``rule(key, value)``. Only entries for
    which it returns ``True`` are passed to the handler.

    The handler is then called as ``handler(key, value)`` and must return
    a transformed ``(key, value)`` pair.

    Intermediate filtered entries are not deeply copied because they are
    immediately passed to the transformation handler. The handler is
    expected to produce appropriate transformed objects for the resulting
    HashMap.

    Every transformed key must be unique. If multiple matching entries
    produce the same key, ``KeyError`` is raised.

    Exceptions raised by either callback are propagated to the caller.

    Args:
      rule: A callable that determines which original entries should be
        transformed.
      handler: A callable that transforms each matching entry into a new
        key-value pair.

    Returns:
      A new HashMap containing the transformed matching entries.

    Raises:
      KeyError: If multiple transformed entries produce the same key.
      TypeError: If a transformed key is not hashable.

    Examples:
      Filter entries before transforming them:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 3,
      ... })
      >>> result = hashmap.filter_then_map(
      ...   lambda key, value: value >= 2,
      ...   lambda key, value: (key.upper(), value * 10),
      ... )
      >>> result.has("A")
      False
      >>> result.get("B")
      20
      >>> result.get("C")
      30
    """
    ...


  @abstractmethod
  def intersect(
    self,
    other: HashMapInterface[K, V],
    deepcopy: bool = False,
  ) -> HashMapInterface[K, V]:
    """
    Return the entries shared by this HashMap and another HashMap.

    An entry is considered shared when the same key exists in both
    HashMaps and their associated values compare equal using ``==``.

    Returned entries follow the current HashMap's iteration order.
    Values involved in the comparison must support equality comparison.

    By default, matching entries are transferred by reference. When
    ``deepcopy`` is ``True``, matching entries are deeply copied so that
    the resulting HashMap is independent from both input HashMaps.

    Args:
      other: The HashMap whose entries should be compared with the current
        instance.
      deepcopy: Whether shared entries should be deeply copied. Defaults
        to ``False``.

    Returns:
      A new HashMap containing entries shared by both HashMaps.

    Examples:
      Return entries present in both HashMaps:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 3,
      ... })
      >>> other = HashMap.from_dict({
      ...   "b": 2,
      ...   "c": 30,
      ... })
      >>> result = hashmap.intersect(other)
      >>> result.has("a")
      False
      >>> result.includes("b", 2)
      True
      >>> result.has("c")
      False

      Equal keys with different values are not considered shared:

      >>> hashmap.intersect(
      ...   HashMap.from_dict({"a": 100})
      ... ).size()
      0
    """
    ...


  @abstractmethod
  def intersect_then_map[RV](
    self,
    other: HashMapInterface[K, V],
    handler: Handler[K, V, RV],
  ) -> HashMapInterface[K, RV]:
    """
    Transform the entries shared by this HashMap and another HashMap.

    An entry is considered shared when the same key exists in both
    HashMaps and their associated values compare equal using ``==``.

    Shared entries follow the current HashMap's iteration order. For each
    shared entry, the handler is called as ``handler(key, value)``, where
    ``value`` is the value from the current HashMap.

    The returned value replaces the original value while the key remains
    unchanged.

    Handler results are stored directly and are not deeply copied. The
    handler is expected to produce appropriate transformed objects.

    Exceptions raised by the handler are propagated to the caller.

    Args:
      other: The HashMap whose entries should be compared with the current
        instance.
      handler: A callable that receives the key and value of each shared
        entry and returns its transformed value.

    Returns:
      A new HashMap containing transformed values for entries shared by
      both HashMaps.

    Examples:
      Transform shared entries:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 2,
      ...   "b": 4,
      ...   "c": 6,
      ... })
      >>> other = HashMap.from_dict({
      ...   "a": 2,
      ...   "b": 10,
      ...   "c": 6,
      ... })
      >>> result = hashmap.intersect_then_map(
      ...   other,
      ...   lambda key, value: value * 10,
      ... )
      >>> result.get("a")
      20
      >>> result.has("b")
      False
      >>> result.get("c")
      60
    """
    ...


  @abstractmethod
  def fold[A](
    self,
    accumulator: A,
    handler: FoldHandler[A, K, V],
    direction: Direction = "left",
  ) -> A:
    """
    Reduce all entries into a single accumulated result.

    The handler is called as ``handler(accumulator, key, value)`` and its
    return value becomes the accumulator for the next entry.

    A direction of ``"left"`` processes entries from the beginning of the
    current iteration order to the end. A direction of ``"right"``
    processes entries from the end to the beginning.

    The supplied accumulator is used directly and is not deeply copied.
    If the HashMap is empty, the original accumulator is returned.

    Exceptions raised by the handler are propagated to the caller.

    Args:
      accumulator: The initial accumulated value.
      handler: A callable that receives the current accumulator, key, and
        value and returns the next accumulated value.
      direction: The direction in which entries should be processed. Must
        be ``"left"`` or ``"right"``. Defaults to ``"left"``.

    Returns:
      The final accumulated result.

    Examples:
      Sum all stored values:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 3,
      ... })
      >>> hashmap.fold(
      ...   0,
      ...   lambda accumulator, key, value:
      ...     accumulator + value,
      ... )
      6

      Build a result using both keys and values:

      >>> hashmap.fold(
      ...   [],
      ...   lambda accumulator, key, value:
      ...     accumulator + [(key, value)],
      ... )
      [('a', 1), ('b', 2), ('c', 3)]
    """
    ...

  @abstractmethod
  def reduce(
    self,
    handler: FoldHandler[V, K, V],
    direction: Direction = "left",
  ) -> V:
    """
    Reduce the HashMap values into a single result.

    Unlike ``fold``, no initial accumulator is supplied explicitly.

    When ``direction`` is ``"left"``, the first value becomes the initial
    accumulator and processing continues from the second entry toward the
    end.

    When ``direction`` is ``"right"``, the last value becomes the initial
    accumulator and processing continues toward the beginning.

    For each remaining entry, the handler is called as
    ``handler(accumulator, key, value)``.

    Exceptions raised by the handler are propagated to the caller.

    Args:
      handler: A callable that receives the current accumulator, key, and
        value and returns the next accumulated value.
      direction: The direction in which entries should be processed. Must
        be ``"left"`` or ``"right"``. Defaults to ``"left"``.

    Returns:
      The final accumulated value.

    Raises:
      ValueError: If the HashMap contains no entries.

    Examples:
      Sum all values:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 1,
      ...   "b": 2,
      ...   "c": 3,
      ... })
      >>> hashmap.reduce(
      ...   lambda accumulator, key, value:
      ...     accumulator + value,
      ... )
      6

      Reducing an empty HashMap raises ``ValueError``:

      >>> HashMap.from_dict({}).reduce(
      ...   lambda accumulator, key, value:
      ...     accumulator + value,
      ... )
      Traceback (most recent call last):
      ...
      ValueError: ...
    """
    ...

  @abstractmethod
  def to_sorted(
    self,
    by: SortCriterion = "value",
    order: Order = "ascending",
    deepcopy: bool = False,
  ) -> HashMapInterface[K, V]:
    """
    Return a sorted copy of the HashMap.

    The current HashMap is never modified. Entries may be sorted by either
    their keys or values and in ascending or descending order.

    Objects used as the selected sorting criterion must support ordering
    with one another. If they cannot be ordered, the resulting
    ``TypeError`` is propagated to the caller.

    Sorting is stable, so entries whose selected sorting values compare
    equally retain their existing relative order.

    By default, the returned HashMap contains references to the same keys
    and values as the current HashMap. When ``deepcopy`` is ``True``, all
    entries are deeply copied before being returned.

    Args:
      by: The component used for sorting. Must be ``"key"`` or
        ``"value"``. Defaults to ``"value"``.
      order: The sorting order. Must be ``"ascending"`` or
        ``"descending"``. Defaults to ``"ascending"``.
      deepcopy: Whether entries in the returned HashMap should be deeply
        copied. Defaults to ``False``.

    Returns:
      A new HashMap containing the entries in the requested order.

    Raises:
      TypeError: If the selected keys or values cannot be ordered with
        one another.

    Examples:
      Return entries sorted by value:

      >>> hashmap = HashMap.from_dict({
      ...   "a": 30,
      ...   "b": 10,
      ...   "c": 20,
      ... })
      >>> sorted_map = hashmap.to_sorted()

      The original HashMap retains its current order while ``sorted_map``
      contains the same entries ordered by value.

      Sort by key in descending order:

      >>> sorted_map = hashmap.to_sorted(
      ...   by="key",
      ...   order="descending",
      ... )

      Request an independent deep copy:

      >>> hashmap = HashMap.from_dict({
      ...   "items": [1, 2],
      ... })
      >>> sorted_map = hashmap.to_sorted(
      ...   deepcopy=True,
      ... )
      >>> sorted_map.get("items").append(3)
      >>> hashmap.get("items")
      [1, 2]
    """
    ...