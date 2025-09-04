from .person import Person


class Venue:
    """
    Represents the club, tracking its state and constraints.
    """

    def __init__(self, capacity: int, constraints: dict[str, float]):
        """
        Initializes the Venue.

        Args:
            capacity (int): The maximum number of people allowed.
            constraints (dict): A dictionary mapping an attribute to the
                                minimum required proportion.
                                e.g., {'local': 0.4, 'all_black': 0.8}
        """
        self.capacity = capacity
        self.constraints = constraints

        self.admitted_people: list[Person] = []
        self.attribute_counts: dict[str, int] = {
            attr: 0 for attr in constraints.keys()
        }

    def __repr__(self) -> str:
        return (f"Venue(admitted={self.get_admitted_count()}/{self.capacity}, "
                f"state={self.get_current_proportions()})")

    def admit(self, person: Person):
        """Adds a person to the venue and updates attribute counts."""
        if self.is_full():
            raise RuntimeError("Cannot admit a person to a full venue.")

        self.admitted_people.append(person)
        for attr, value in person.attributes.items():
            if attr in self.attribute_counts and value:
                self.attribute_counts[attr] += 1

    def is_full(self) -> bool:
        """Checks if the venue has reached its capacity."""
        return len(self.admitted_people) >= self.capacity

    def get_admitted_count(self) -> int:
        """Returns the current number of people in the venue."""
        return len(self.admitted_people)

    def get_current_proportions(self) -> dict[str, float]:
        """Calculates the current proportion of each attribute."""
        current_count = self.get_admitted_count()
        if current_count == 0:
            return {attr: 0.0 for attr in self.attribute_counts}

        return {
            attr: count / current_count
            for attr, count in self.attribute_counts.items()
        }

    def check_constraints_met(self) -> bool:
        """
        Checks if the current state of the venue satisfies all constraints.
        This is primarily for the end-of-game evaluation.
        """
        if not self.is_full():
            return False

        current_proportions = self.get_current_proportions()
        for attr, required_prop in self.constraints.items():
            if current_proportions.get(attr, 0.0) < required_prop:
                return False
        return True
