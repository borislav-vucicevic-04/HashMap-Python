from hashmap import HashMap

def make_hashmap[K, V](
  dictionary: dict[K, V],
) -> HashMap[K, V]:
  hashmap: HashMap[K, V] = HashMap[K, V].from_dict(
    dictionary
  )

  return hashmap

class EqualityValue:
  def __init__(self, value: int) -> None:
    self.value = value

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, EqualityValue):
      return False

    return self.value == other.value