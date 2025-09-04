from .base_bouncer import BaseBouncer
from ..simulation.person import Person
from ..simulation.venue import Venue


class GreedyBouncer(BaseBouncer):
    """
    A simple baseline bouncer that makes decisions greedily.

    It identifies the constraint that is furthest from being met
    and admits anyone who satisfies that specific attribute.
    """

    def should_admit(self, person: Person, venue: Venue) -> bool:
        """
        Admits a person if they have the attribute that is currently
        most 'in need'.
        """
        current_proportions = venue.get_current_proportions()

        # If the venue is empty, admit the first person to get some data.
        if venue.get_admitted_count() == 0:
            return True

        # Calculate the 'need' for each attribute.
        # Need = Required Proportion - Current Proportion
        needs = {
            attr: venue.constraints[attr] - current_proportions[attr]
            for attr in venue.constraints
        }

        # If all needs are negative (i.e., all constraints are currently met),
        # the bouncer can be lenient. Let's admit everyone.
        if all(n <= 0 for n in needs.values()):
            return True

        # Find the attribute with the highest need.
        most_needed_attr = max(needs.keys(), key=lambda k: needs[k])

        # Admit the person if they have this most needed attribute.
        return person.attributes.get(most_needed_attr, False)
