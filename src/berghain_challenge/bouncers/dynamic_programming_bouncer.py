from .base_bouncer import BaseBouncer
from ..simulation.person import Person
from ..simulation.venue import Venue


class DpBouncer(BaseBouncer):
    """
    A bouncer that uses a heuristic inspired by dynamic programming.

    It calculates a 'value score' for each person based on the scarcity
    of their attributes and admits them if they exceed a dynamic threshold
    that increases as the venue fills.
    """

    def __init__(self, start_threshold: float = 0.0, end_threshold: float = 0.1):
        """
        Initializes the bouncer with threshold parameters.

        Args:
            start_threshold: The initial score required for admission.
            end_threshold: The score required for admission when the venue is nearly full.
        """
        self.start_threshold = start_threshold
        self.end_threshold = end_threshold

    def _calculate_person_score(self, person: Person, venue: Venue) -> float:
        """Calculates the value of admitting a person right now."""
        if venue.get_admitted_count() == 0:
            return 1.0

        score = 0.0
        current_proportions = venue.get_current_proportions()

        # This represents the 'option value' of an attribute.
        BASE_ATTRIBUTE_VALUE = 0.01

        for attr, has_attr in person.attributes.items():
            if has_attr and attr in venue.constraints:
                required_prop = venue.constraints[attr]
                current_prop = current_proportions.get(attr, 0.0)

                # The 'need' is still the primary driver of the score.
                need = max(0, required_prop - current_prop)

                # --- CHANGE: Add the need and the base value ---
                # A person gets a small score just for having a useful trait,
                # and a large score for having a trait that is needed.
                score += need + BASE_ATTRIBUTE_VALUE

        return score

    def _calculate_current_threshold(self, venue: Venue) -> float:
        """Calculates the minimum score needed for admission at the current fill level."""

        # Calculate the fullness of the venue as a fraction (0.0 to 1.0)
        fullness = venue.get_admitted_count() / venue.capacity
        if fullness >= 1.0:
            return float('inf')  # If full, threshold is insurmountable.

        # Linearly interpolate between the start and end thresholds
        # The formula is: start + (end - start) * progress
        threshold = self.start_threshold + \
            (self.end_threshold - self.start_threshold) * fullness

        return threshold

    def should_admit(self, person: Person, venue: Venue) -> bool:
        """
        Admits a person if their score exceeds the current dynamic threshold.
        """
        score = self._calculate_person_score(person, venue)
        threshold = self._calculate_current_threshold(venue)

        return score >= threshold
