from abc import ABC, abstractmethod
from ..simulation.person import Person
from ..simulation.venue import Venue


class BaseBouncer(ABC):
    """
    Abstract base class defining the interface for all bouncer models.
    """
    @abstractmethod
    def should_admit(self, person: Person, venue: Venue) -> bool:
        """
        The core decision-making logic for the bouncer.

        Args:
            person: The Person object arriving at the door.
            venue: The current state of the Venue.

        Returns:
            True if the person should be admitted, False otherwise.
        """
        pass
