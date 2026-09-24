from typing import Callable, Literal


type Direction = Literal["left", "right"]
"""
Direction in which an ordered HashMap operation is performed.

Values:
  "left": Process entries from the beginning of the current iteration
    order toward the end.
  "right": Process entries from the end of the current iteration order
    toward the beginning.
"""


type Order = Literal["ascending", "descending"]
"""
Sorting order used by HashMap sorting operations.

Values:
  "ascending": Sort entries from lowest to highest according to the
    selected sorting criterion.
  "descending": Sort entries from highest to lowest according to the
    selected sorting criterion.
"""


type SortCriterion = Literal["key", "value"]
"""
Component of a HashMap entry used for sorting.

Values:
  "key": Sort entries according to their keys.
  "value": Sort entries according to their values.
"""


type Callback[K, V] = Callable[[K, V], None]
"""
Callback executed for a HashMap entry.

The callback receives the entry's key followed by its associated value
and does not produce a return value.

Signature:
  callback(key, value) -> None

Type Parameters:
  K: Type of the entry key.
  V: Type of the entry value.
"""


type Handler[K, V, R] = Callable[[K, V], R]
"""
Callback that transforms or processes a HashMap entry.

The handler receives the entry's key followed by its associated value
and returns a result.

Signature:
  handler(key, value) -> result

Type Parameters:
  K: Type of the entry key.
  V: Type of the entry value.
  R: Type of the returned result.
"""


type UpdateHandler[V] = Callable[[V, V], V]
"""
Callback used to update an existing value.

The handler receives the currently stored value followed by the new
value supplied to the operation. Its return value becomes the new value
associated with the key.

Signature:
  handler(old_value, new_value) -> value

Type Parameters:
  V: Type of the stored and returned value.
"""


type SetHandler[V] = Callable[[V | None, V], V]
"""
Callback used to set a value.

The handler receives the currently stored value followed by the new
value supplied to the operation. If the key does not exist, the first
argument is ``None``.

The returned value becomes the value associated with the key.

Signature:
  handler(old_value, new_value) -> value

Type Parameters:
  V: Type of the stored and returned value.
"""


type ReplaceHandler[K, OV, NV] = Callable[[K, OV, NV], OV]
"""
Callback used to replace an existing value during a bulk operation.

The handler receives the key, the value currently stored in the target
HashMap, and the corresponding incoming value.

Its return value becomes the new value stored in the target HashMap.

Signature:
  handler(key, old_value, new_value) -> old_value_type

Type Parameters:
  K: Type of the entry key.
  OV: Type of values stored in the target HashMap.
  NV: Type of incoming values.
"""


type MergeHandler[K, OV, NV] = Callable[[K, OV | None, NV], OV]
"""
Callback used to merge entries during a bulk operation.

The handler receives the key, the currently stored value, and the
incoming value.

If the key does not exist in the target HashMap, the stored value is
``None``.

The returned value becomes the value associated with the key.

Signature:
  handler(key, old_value, new_value) -> merged_value

Type Parameters:
  K: Type of the entry key.
  OV: Type of values stored in the target HashMap.
  NV: Type of incoming values.
"""


type FoldHandler[A, K, V] = Callable[[A, K, V], A]
"""
Callback used to accumulate HashMap entries into a single result.

The handler receives the current accumulator, the entry key, and the
entry value. Its return value becomes the accumulator for the next
iteration.

Signature:
  handler(accumulator, key, value) -> accumulator

Type Parameters:
  A: Type of the accumulator.
  K: Type of the entry key.
  V: Type of the entry value.
"""


type Rule[K, V] = Callable[[K, V], bool]
"""
Predicate used to test a HashMap entry.

The rule receives the entry's key followed by its associated value and
returns ``True`` when the entry satisfies the condition.

Signature:
  rule(key, value) -> bool

Type Parameters:
  K: Type of the entry key.
  V: Type of the entry value.
"""