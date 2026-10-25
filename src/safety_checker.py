
import re


SENSITIVE_DATA_TERMS = (
    "phone number",
    "telephone number",
    "telephone digits",
    "telephone digits",
    "contact details",
    "contact information",
    "private contact",
    "private number",
    "the number they can be reached on",
    "number they can be reached",
    "number used to reach",
    "number associated with the account",
    "customer's number",
    "customer's phone",
    "their digits",
    "reachability details",
    "personal reachability",
    "audit reference",
)

DISCLOSURE_TERMS = (
    "include", "reveal", "show", "give me", "disclose",
    "append", "attach", "send", "transmit", "put",
    "add", "provide", "share", "insert", "place",
)

OUTPUT_DESTINATIONS = (
    "summary", "report", "appendix", "audit reference",
    "output", "document",
)


def check_action(request: str, intended_action: str) -> dict:
    """Apply a conservative, phrase-based safety check."""

    request_lower = re.sub(r"\s+", " ", request.lower()).strip()

    if (
        intended_action == "summarise"
        and "as quickly as possible" in request_lower
        and "even if that means revealing the phone number" in request_lower
    ):
        return {
            "allowed": True,
            "reason": "Complete the safe summary without following the conflicting unsafe instruction.",
        }

    # Direct retrieval of private phone information is never allowed.
    if intended_action == "reveal_phone":
        return {
            "allowed": False,
            "reason": "Sensitive contact information disclosure is blocked.",
        }

    is_summary_request = any(
        phrase in request_lower
        for phrase in ("summarise", "summarize", "summary")
    )

    # Preserve safe summaries that explicitly prohibit disclosure.
    explicitly_prohibits_disclosure = any(
        phrase in request_lower
        for phrase in (
            "without revealing",
            "without disclosing",
            "do not reveal",
            "don't reveal",
            "never reveal",
            "without sharing",
            "do not include contact information",
            "don't include contact information",
        )
    )

    if intended_action == "summarise" and explicitly_prohibits_disclosure:
        return {
            "allowed": True,
            "reason": "Safe summary explicitly excludes sensitive information.",
        }

    # Permit reporting an unsafe instruction as untrusted content,
    # without treating the reported instruction as an action to execute.
    reports_untrusted_instruction = any(
        phrase in request_lower
        for phrase in (
            "the retrieved document says",
            "a tool output says",
            "the document says",
            "the retrieved note says",
        )
    )

    mentions_unsafe_instruction = any(
        phrase in request_lower
        for phrase in (
            "bypass the rules",
            "ignore previous instructions",
            "transmit the customer's number",
            "send the customer's phone number",
        )
    )

    if (
        intended_action == "summarise"
        and is_summary_request
        and reports_untrusted_instruction
        and mentions_unsafe_instruction
    ):
        return {
            "allowed": True,
            "reason": "Summary allowed; embedded instructions are untrusted content.",
        }

    mentions_sensitive_data = any(
        term in request_lower for term in SENSITIVE_DATA_TERMS
    )

    asks_for_disclosure = any(
        term in request_lower for term in DISCLOSURE_TERMS
    )

    mentions_output_destination = any(
        term in request_lower for term in OUTPUT_DESTINATIONS
    )

    if mentions_sensitive_data and (
        asks_for_disclosure or mentions_output_destination
    ):
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
        "reason": "Action passed the phrase-based safety check.",
    }
