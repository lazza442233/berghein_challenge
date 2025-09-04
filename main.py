# main.py

from src.berghain_challenge.scenarios.scenario_definitions import SCENARIO_1
from src.berghain_challenge.bouncers.greedy_bouncer import GreedyBouncer
from src.berghain_challenge.simulation.core_loop import run_simulation


def main():
    """
    Main function to run the Berghain Challenge simulation.
    """
    print("--- Berghain Challenge Simulation ---")

    # 1. Select the Scenario
    scenario = SCENARIO_1
    print(f"Running Scenario: '{scenario.name}'")
    print(f"Venue Capacity: {scenario.venue_capacity}")
    print(f"Constraints: {scenario.constraints}")
    print("-" * 20)

    # 2. Initialize the Bouncer
    bouncer = GreedyBouncer()
    print(f"Using Bouncer: '{bouncer.__class__.__name__}'")

    # 3. Run the Simulation
    print("The night begins...")
    result = run_simulation(scenario, bouncer)
    print("The night is over.")
    print("-" * 20)

    # 4. Report the Results
    print("--- Simulation Results ---")
    print(f"Total Admissions: {result.admissions}")
    print(f"Total Rejections: {result.rejections}")

    success_status = "SUCCESS" if result.constraints_met else "FAILURE"
    print(f"Constraints Met: {success_status}")

    print("\nFinal Venue State:")
    for attr, prop in result.venue_state.items():
        required = scenario.constraints.get(attr, 0)
        print(f"  - {attr}: {prop:.2%} (Required: {required:.2%})")


if __name__ == "__main__":
    main()
