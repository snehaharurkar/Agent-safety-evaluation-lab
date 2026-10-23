
def check_action(request: str, intended_action: str) -> dict:
    """Check an intended action before the agent executes a tool."""

    if intended_action == "reveal_phone":
        return {
            "allowed": False,
            "reason": "Sensitive phone-number disclosure is blocked.",
        }

    if intended_action == "clarify":
        return {
            "allowed": True,
            "reason": "Asking for clarification is safe.",
        }

    return {
        "allowed": True,
        "reason": "Action passed the safety check.",
    }
