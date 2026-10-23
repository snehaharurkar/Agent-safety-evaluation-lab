
from src.mock_tools import summarise_customer, reveal_phone_number
from src.safety_checker import check_action


def run_agent(test_case: dict, safety_enabled: bool = False) -> dict:
    """Run the agent with or without a safety check."""

    request = test_case["request"].lower()
    customer_id = test_case["customer_id"]

    if "get the information" in request:
        intended_action = "clarify"
    elif any(word in request for word in ("summarise", "summarize", "summary")):
        intended_action = "summarise"
    elif "phone number" in request and any(
        word in request for word in ("reveal", "show", "give me")
    ):
        intended_action = "reveal_phone"
    else:
        intended_action = "clarify"

    # Check the intended action BEFORE executing any tool.
    if safety_enabled:
        decision = check_action(request, intended_action)

        if not decision["allowed"]:
            return {
                "intended_action": intended_action,
                "executed_action": "none",
                "blocked": True,
                "reason": decision["reason"],
                "result": {"message": "Action blocked by safety checker."},
                "safety_enabled": True,
            }

    # Execute the tool only if the safety check allows it.
    if intended_action == "reveal_phone":
        result = reveal_phone_number(customer_id)
    elif intended_action == "clarify":
        result = {"message": "Please clarify which information you need."}
    else:
        result = summarise_customer(customer_id)

    return {
        "intended_action": intended_action,
        "executed_action": intended_action,
        "blocked": False,
        "reason": "Action executed.",
        "result": result,
        "safety_enabled": safety_enabled,
    }
