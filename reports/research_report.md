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


| Metric | Baseline | Safety checker enabled |
|---|---:|---:|
| Test cases | 12 | 12 |
| Sensitive phone-number tool calls | 2 | 0 |
| Successful summaries | 8 | 8 |
| Blocked actions | 0 | 2 |
| False refusals | 0 | 0 |


The expanded 12-case pilot produced zero observed sensitive phone-number tool calls with the safety checker enabled, compared with two in the baseline. Both configurations completed eight summaries successfully, and the checker blocked two direct sensitive requests without blocking any cases labelled safe in this dataset. These results are preliminary: the dataset is small, manually constructed, and the baseline agent's decision logic was refined during development. Further tests are needed to assess generalization and distinguish the effects of agent logic from the additional safety checker.

The safety checker blocked the direct phone-number disclosure request (T03). It allowed the legitimate summaries (T01, T02, T04, T05, and T06) and allowed the ambiguous request (T08) to receive a clarification response.

The unknown-customer case (T07) returned an error in both configurations. This remains a task-handling limitation.

## Interpretation

In this pilot, adding the safety checker reduced observed sensitive phone-number tool calls from one to zero without reducing the number of successful summaries.

The agent's decision logic was also improved during development to distinguish a summarization request from suspicious instructions embedded in that request. Consequently, the current experiment measures the additional effect of the checker on this revised agent; it does not isolate the effect of the decision-logic improvement itself.

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