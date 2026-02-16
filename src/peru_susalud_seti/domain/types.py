from abc import ABC, abstractmethod
from typing import Any, List

class Observer(ABC):
    """
    Observer Interface: Defines the contract for objects that listen strictly
    to validation or generation events.
    """
    @abstractmethod
    def update(self, event_type: str, message: str, data: Any = None) -> None:
        pass

class Subject(ABC):
    """
    Subject Base Class: Manages the subscription of observers.
    Used by Generators/Validators to notify issues without coupling.
    """
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event_type: str, message: str, data: Any = None) -> None:
        for observer in self._observers:
            observer.update(event_type, message, data)