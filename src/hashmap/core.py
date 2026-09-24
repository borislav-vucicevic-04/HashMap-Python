from .__types__ import *
from .__mixins__ import *

class HashMap[K, V](
  HashMapInterface[K, V]
): 
  def __init__(self) -> None:
    super().__init__()