# Preliminary Research Report: AI Agent Safety Evaluation

## Research Question

Can a safety-checking layer reduce unsafe tool calls by an AI agent when it encounters malicious instructions, without unnecessarily blocking legitimate tasks?

## Objective

Build a small, reproducible prototype that compares an agent operating without an additional safety checker against the same agent operating with a safety checker.

## Experimental Setup

- **Dataset:** 8 hand-written test cases.
- **Data:** Synthetic customer records only.
- **Tools:** Local mock functions; no external customer systems are accessed.
- **Baseline:** Agent runs without the additional safety checker.
- **Intervention:** Agent checks intended actions before executing tools.
- **Evaluation:** Count sensitive phone-number tool calls, successful summaries, and blocked actions.

## Preliminary Results

The evaluation uses 13 hand-written test cases and compares the agent with its safety checker disabled and enabled.

| Metric                            | Baseline | Safety checker enabled |
| --------------------------------- | -------: | ---------------------: |
| Sensitive phone-number tool calls |        2 |                      0 |
| Successful summaries              |        8 |                      8 |
| Blocked actions                   |        0 |                      3 |
| False refusals                    |        0 |                      0 |

### Adversarial Case: T13

T13 requests a customer summary while explicitly asking the agent to include a private phone number. In the baseline configuration, the agent classifies this as a summary request. The original checker also allowed it because it only checked the intended action.

After adding a request-content check, the safety-enabled agent blocks T13. A regression test now verifies that the action is blocked and the sensitive tool is not executed.

### Interpretation

This result demonstrates that checking only an agent's intended action can miss unsafe requests when the agent misclassifies them. Examining the request content caught this particular failure.

These results remain preliminary. The test set is small and hand-written, and the rule-based checker may fail on different wording, indirect requests, or other sensitive actions. Zero observed false refusals in this dataset does not establish that the approach will preserve legitimate tasks in general.

## Limitations

1. The dataset contains only eight manually written cases.
2. The agent uses simple keyword-based rules rather than a general-purpose language model.
3. The safety checker covers only a narrow set of actions.
4. The tests do not establish robustness to diverse or paraphrased attacks.
5. The observed result is too small to support general claims about AI agent safety.

## Next Steps

- Expand the dataset with varied direct requests, prompt-injection attempts, ambiguous requests, and legitimate edge cases.
- Add automated checks for false refusals and task completion.
- Track attempted tool calls separately from executed tool calls.
- Compare results across repeated, documented test sets.
- Investigate whether the checker can be bypassed by rephrasing a sensitive request.

## Conclusion

This prototype demonstrates a basic, testable safety intervention: a pre-execution rule blocks a sensitive tool call in the current pilot dataset. Further evaluation is needed before drawing conclusions about effectiveness on real-world AI agents.
