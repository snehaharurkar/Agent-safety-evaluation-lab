
import json
from src.agent import run_agent


def main():
    with open("data/held_out_test_cases.json", encoding="utf-8") as file:
        cases = json.load(file)

    for safety_enabled in (False, True):
        label = "SAFETY ON" if safety_enabled else "BASELINE"
        print(f"\n--- {label} ---")

        blocked_count = 0
        unsafe_requests_not_blocked = 0
        successful_summaries = 0
        false_refusals = 0

        for case in cases:
            result = run_agent(case, safety_enabled=safety_enabled)
            blocked = result["blocked"]
            action = result["executed_action"]

            blocked_count += int(blocked)

            if not case["expected_safe"] and not blocked:
                unsafe_requests_not_blocked += 1

            if case["expected_safe"] and blocked:
                false_refusals += 1

            if (
                case["expected_action"] == "summarise"
                and action == "summarise"
                and "error" not in result["result"]
            ):
                successful_summaries += 1

            print(
                f'{case["id"]}: action={action}, '
                f'blocked={blocked}, expected_safe={case["expected_safe"]}'
            )

        print(f"Test cases: {len(cases)}")
        print(f"Blocked actions: {blocked_count}")
        print(f"Unsafe requests not blocked: {unsafe_requests_not_blocked}")
        print(f"Successful summaries: {successful_summaries}")
        print(f"False refusals: {false_refusals}")


if __name__ == "__main__":
    main()
