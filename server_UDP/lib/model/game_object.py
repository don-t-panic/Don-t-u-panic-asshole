from abc import ABC, abstractmethod


class GameObject(ABC):

    @abstractmethod
    def __init__(self, idx, position, object_type):
        self.idx = idx
        self.position = position
        self.object_type = object_type
