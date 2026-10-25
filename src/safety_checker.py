
def check_action(request: str, intended_action: str) -> dict:
    """Check an intended action and request content before tool execution."""

    request_lower = request.lower()

    # Block requests that explicitly seek private phone-number disclosure,
    # even when framed as another task such as summarisation.

    requests_sensitive_disclosure = (
        any(
            phrase in request_lower
            for phrase in (
                "phone number",
                "contact details",
                "private contact",
            )
        )
        and any(
            phrase in request_lower
            for phrase in (
                "include",
                "reveal",
                "show",
                "give me",
                "disclose",
                "private",
                "append",
            )
        )
    )

    if intended_action == "reveal_phone" or requests_sensitive_disclosure:
        return {
            "allowed": False,
            "reason": "Sensitive contact information disclosure is blocked.",
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
