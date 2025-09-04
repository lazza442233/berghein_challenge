import random
from dataclasses import dataclass


@dataclass
class Scenario:
    """Defines the rules and distributions for a single simulation run."""
    name: str
    venue_capacity: int
    rejection_limit: int
    constraints: dict[str, float]
    # P(attribute=True)
    attribute_probabilities: dict[str, float]
    # P(attr2=True | attr1=True)
    conditional_probabilities: dict[tuple[str, str], float]


def generate_person(scenario: Scenario) -> 'Person':
    """
    Generates a single Person instance based on the scenario's probabilities.

    This is a simplified generator that handles one level of dependency.
    For example, it can model how being a 'regular' might influence
    the chance of wearing 'all_black'.
    """
    from ..simulation.person import Person

    attributes = {}

    sorted_attrs = sorted(scenario.attribute_probabilities.keys())

    for attr in sorted_attrs:
        dependency = None
        for (attr2, attr1), prob in scenario.conditional_probabilities.items():
            if attr2 == attr and attr1 in attributes:
                base_attr_value = attributes[attr1]
                if base_attr_value is True:
                    dependency = prob
                break

        prob = dependency if dependency is not None else scenario.attribute_probabilities[
            attr]
        attributes[attr] = random.random() < prob

    return Person(attributes)

# --- SCENARIO DEFINITIONS ---


SCENARIO_1 = Scenario(
    name="Classic Berlin Night",
    venue_capacity=1000,
    rejection_limit=20000,
    constraints={
        'local': 0.40,      # At least 40% must be Berlin locals
        'all_black': 0.80,  # At least 80% must be wearing all black
    },
    # Base probabilities for an arriving person
    attribute_probabilities={
        'local': 0.50,      # 50% of people in the queue are locals
        'all_black': 0.70,  # 70% of people in the queue wear all black
        'regular': 0.20,    # 20% of people in the queue are regulars
    },
    # Conditional probabilities to model correlations
    # P(attr2=True | attr1=True)
    conditional_probabilities={
        # Regulars are more likely to wear all black.
        # If a person is a regular, their chance of wearing all black is 90%.
        ('all_black', 'regular'): 0.90,
    }
)
