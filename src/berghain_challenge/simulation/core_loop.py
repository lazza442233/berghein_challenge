from dataclasses import dataclass
from ..scenarios.scenario_definitions import Scenario, generate_person
from ..bouncers.base_bouncer import BaseBouncer
from .venue import Venue


@dataclass
class SimulationResult:
    """Stores the results of a single simulation run."""
    rejections: int
    admissions: int
    constraints_met: bool
    venue_state: dict[str, float]


def run_simulation(scenario: Scenario, bouncer: BaseBouncer) -> SimulationResult:
    """
    Runs a single episode of the Berghain Challenge.

    Args:
        scenario: The Scenario object defining the rules.
        bouncer: The Bouncer object that will make decisions.

    Returns:
        A SimulationResult object summarizing the outcome.
    """
    venue = Venue(capacity=scenario.venue_capacity,
                  constraints=scenario.constraints)
    rejections = 0

    while not venue.is_full() and rejections < scenario.rejection_limit:
        # A new person arrives
        person = generate_person(scenario)

        # The bouncer makes a decision
        if bouncer.should_admit(person, venue):
            venue.admit(person)
        else:
            rejections += 1

    # The night is over. Collect the results.
    return SimulationResult(
        rejections=rejections,
        admissions=venue.get_admitted_count(),
        constraints_met=venue.check_constraints_met(),
        venue_state=venue.get_current_proportions()
    )
