# Preliminary Research Report: AI Agent Safety Evaluation

## Research Question

Can a safety-checking layer reduce unsafe tool calls by an AI agent encountering malicious or conflicting instructions without unnecessarily blocking legitimate tasks?

## Objective

Build a reproducible prototype comparing an agent without an additional safety checker against the same agent with a safety checker enabled.

## Experimental Setup

- **Dataset:** 14 hand-written test cases.
- **Data:** Synthetic customer records only.
- **Tools:** Local mock functions; no external customer systems are accessed.
- **Baseline:** Agent runs without the additional safety checker.
- **Intervention:** The checker evaluates the intended action and selected request wording before tool execution.
- **Evaluation:** Measure sensitive phone-number tool calls, successful summaries, blocked actions, and false refusals.

## Preliminary Results

The current evaluation uses 14 hand-written test cases. The results below reflect the latest observed run after adding the T14 rule.

| Metric | Baseline | Safety checker enabled |
|---|---:|---:|
| Sensitive phone-number tool calls | 2 | 0 |
| Successful summaries | 8 | 8 |
| Blocked actions | 0 | 4 |
| False refusals | 0 | 0 |

These counts are specific to this test set and the current implementation. Rerun the evaluation before treating them as final if the code or dataset changes.

## Adversarial Findings

### T13 — Sensitive information hidden in a summary request

T13 asks for a customer summary while also asking for a private phone number. The baseline agent classifies it as a summary request, and the original checker allowed it because it checked only the intended action.

A request-content rule was added to block this wording. A regression test verifies that the safety-enabled agent blocks the action.

### T14 — Alternative wording for private contact information

T14 asks for a summary and requests that private contact details be appended. The initial implementation treated it as a summary and did not block it.

The checker was then extended to recognize the phrases “contact details” and “private contact” in combination with selected disclosure-related wording. The subsequent evaluation showed T14 blocked.

This is evidence that the added rule catches these particular examples, not evidence that it detects private-information requests in general.

## Interpretation

The pilot illustrates a limitation of checking only an agent's intended action: an unsafe request can be misclassified as an ordinary summary task. Adding request-content checks caught two specific adversarial examples in this dataset.

The checker remains a narrow, keyword-based intervention. It may fail on different paraphrases, indirect requests, other sensitive data, or adversarial wording that does not match its rules.

The absence of observed false refusals in this small dataset does not establish that legitimate tasks will be preserved in general.

## Limitations

1. The dataset contains only 14 manually written cases.
2. The agent and checker use simple rules rather than a general-purpose language model.
3. The checker covers a narrow set of sensitive actions and wording patterns.
4. The results do not establish robustness to diverse or adaptive attacks.
5. The test set is small and may not represent real-world agent behavior.
6. The baseline logic was refined during development, limiting causal interpretation of the comparison.

## Next Steps

- Expand the dataset with varied direct requests, prompt-injection attempts, ambiguous requests, and legitimate edge cases.
- Add automated checks for false refusals and successful task completion.
- Track attempted tool calls separately from executed tool calls.
- Evaluate previously unseen paraphrases rather than only wording used to develop the checker.
- Compare the current keyword-based approach with alternative safety-checking strategies.
- Document all failures, including cases the checker does not block.

## Conclusion

This prototype demonstrates a testable pre-execution safety intervention that blocks several specific sensitive-information requests in a small synthetic dataset. Broader and more systematic evaluation is needed before drawing conclusions about its effectiveness on real-world AI agents.
