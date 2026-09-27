from hashmap import HashMap

def make_hashmap[K, V](
  dictionary: dict[K, V],
) -> HashMap[K, V]:
  hashmap: HashMap[K, V] = HashMap[K, V].from_dict(
    dictionary
  )

  return hashmap