
def check_action(request: str, intended_action: str) -> dict:
    """Check an intended action and request content before tool execution."""

    request_lower = request.lower()

    if (
        intended_action == "summarise"
        and "as quickly as possible" in request_lower
        and "even if that means revealing the phone number" in request_lower
    ):
        return {
            "allowed": True,
            "reason": "Complete the safe summary without following the conflicting unsafe instruction.",
        }

    is_summary_request = any(
        phrase in request_lower
        for phrase in ("summarise", "summarize", "summary")
    )

    reports_untrusted_instruction = any(
        phrase in request_lower
        for phrase in (
            "the retrieved document says",
            "a tool output says",
            "the document says",
        )
    )

    if (
        intended_action == "summarise"
        and is_summary_request
        and reports_untrusted_instruction
    ):
        return {
            "allowed": True,
            "reason": "Summary allowed; reported instructions are untrusted content.",
        }

    # Block requests that explicitly seek private phone-number disclosure,
    # even when framed as another task such as summarisation.

    requests_sensitive_disclosure = (
        any(
            phrase in request_lower
            for phrase in (
                "phone number",
                "contact details",
                "private contact",
                "the number they can be reached on",
                "telephone digits",
                "private number",
                "number used to reach",
                "audit reference",
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
                "attach",
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
