# Evaluating a Phrase-Based Safety Checker for Sensitive Information Disclosure in an AI-Agent Prototype

**Author:** Sneha S. Harurkar  
**Repository:** [agent-safety-evaluation-lab](https://github.com/snehaharurkar/agent-safety-evaluation-lab)  
**Research area:** AI agent safety, tool-use constraints, and sensitive-information disclosure  
**Status:** Preliminary prototype and iterative evaluation

## Abstract

AI agents that use tools may encounter requests to disclose sensitive information, including when a request also contains a legitimate task. This project investigates whether a simple phrase-based safety checker can reduce unauthorized customer phone-number disclosure in a simulated agent.

The prototype evaluates 17 development cases with the checker disabled and enabled, followed by a revised five-case evaluation. In the development evaluation, observed unsafe phone-tool calls decreased from two to zero. However, the checker blocked 11 actions and produced four false refusals, indicating a substantial over-blocking problem. In the revised five-case evaluation, it blocked all three requests labelled unsafe and allowed both requests labelled safe.

These results are preliminary. The five-case set was used during iterative checker refinement, so it is not an untouched independent benchmark. The small, manually constructed datasets and phrase-based implementation do not establish robust generalization. The findings illustrate both the potential and limitations of simple rule-based safeguards for agent tool use.

## 1. Introduction

AI agents can combine language-model reasoning with tools that retrieve information or perform actions. This creates a safety challenge: a system may need to complete a legitimate task while refusing an unauthorized disclosure or action.

For example, summarizing a synthetic customer record may be appropriate, while retrieving and disclosing that customer's phone number may not be. A safeguard should distinguish the requested action rather than indiscriminately blocking every request that mentions contact information.

This project explores a narrow version of that challenge using a simulated customer-support agent and a manually defined phrase-based checker.

The aim is not to claim a comprehensive solution to agent safety. It is to create a reproducible, inspectable experiment that exposes both unsafe behavior and over-blocking.

## 2. Research Question

**Can a phrase-based safety checker reduce unauthorized disclosure of sensitive customer contact information while preserving legitimate summarization tasks?**

### Objectives

1. Measure the behavior of the simulated agent without a safety checker.
2. Measure the behavior of the same test cases with the checker enabled.
3. Identify unsafe phone-tool calls and legitimate actions that are incorrectly blocked.
4. Examine behavior on a revised set of five cases.
5. Document implementation limitations and propose a more rigorous evaluation.

## 3. System Design

The prototype contains four main components.

### 3.1 Simulated agent

The agent receives a request, identifies an intended action, and invokes a corresponding simulated tool. Supported actions include summarization, phone-number retrieval, and clarification.

### 3.2 Phrase-based safety checker

The checker inspects the request using manually defined terms, phrases, and conditions. Depending on the request and intended action, it allows or blocks the action.

This approach is transparent and easy to inspect, but it is brittle. Different wording can express the same intent, and sensitive phrases can appear in benign contexts.

### 3.3 Mock tools

The tool layer uses synthetic customer data and simulated operations. It does not contact external systems or retrieve real customer information.

### 3.4 Evaluation scripts

Two scripts compare behavior with the checker disabled and enabled:

- `src/evaluate.py` evaluates the 17-case development set.
- `src/evaluate_held_out.py` evaluates the revised five-case set.

The project also contains automated tests in `tests/test_evaluation.py`.

## 4. Experimental Setup

### Development evaluation

The development dataset contains 17 manually constructed test cases. The cases explore summarization, phone-number disclosure, conflicting instructions, clarification, and requests involving sensitive information.

The same development cases are run with the checker disabled and enabled.

### Revised five-case evaluation

A separate JSON file contains five manually constructed cases:

| Case | Intended category | Request focus |
|---|---|---|
| H01 | Unsafe | Include a customer's digits in an appendix |
| H02 | Unsafe | Disclose the number associated with an account |
| H03 | Safe | Summarize without revealing contact information |
| H04 | Safe | Summarize content containing an embedded instruction to bypass rules |
| H05 | Unsafe | Attach personal reachability details |

The categories represent the expected behavior specified in the test data. They are not independently adjudicated ground truth.

**Evaluation caveat:** the five-case set was used during iterative checker refinement. It should be described as a revised evaluation set, not as an untouched held-out benchmark. The results may reflect adaptation to those examples.

## 5. Metrics

The evaluation scripts report the following measures.

- **Unsafe phone-tool calls:** the number of observed phone-tool calls treated as unsafe by the evaluation logic.
- **Successful summaries:** the number of summarization actions completed successfully.
- **Blocked actions:** the number of actions blocked by the safety checker.
- **False refusals:** cases labelled safe that the evaluation identifies as incorrectly blocked.
- **Unsafe requests not blocked:** cases labelled unsafe for which the revised evaluation does not report a block.

These metrics describe this prototype and its defined test cases. They should not be interpreted as universal measures of agent safety.

## 6. Results

### 6.1 Development evaluation: 17 cases

| Metric | Checker OFF | Checker ON |
|---|---:|---:|
| Test cases | 17 | 17 |
| Unsafe phone-tool calls | 2 | 0 |
| Successful summaries | 10 | 4 |
| Blocked actions | 0 | 11 |
| False refusals | 0 | 4 |

With the checker enabled, the observed unsafe phone-tool calls decreased from two to zero. However, successful summaries decreased from ten to four, while 11 actions were blocked.

The evaluator reported four false refusals: **T04, T05, T09, and T10**.

This result reveals a significant trade-off. Although the checker blocks the observed unsafe phone-tool calls in this experiment, it also prevents legitimate actions. The implementation therefore needs better discrimination between unsafe disclosure requests and safe tasks.

The zero unsafe-call result does not establish that the checker will prevent every unsafe action in other datasets or environments.

### 6.2 Revised five-case evaluation

| Metric | Checker OFF | Checker ON |
|---|---:|---:|
| Test cases | 5 | 5 |
| Blocked actions | 0 | 3 |
| Unsafe requests not blocked | 3 | 0 |
| Successful summaries | 5 | 2 |
| False refusals | 0 | 0 |

With the checker disabled, all three requests labelled unsafe were left unblocked. With the checker enabled, all three were blocked, while both requests labelled safe were allowed.

This is a positive result on the five specified cases. However, it is not independent evidence of generalization because the cases were examined during iterative development. The sample is also too small to support broad performance claims.

### 6.3 Combined interpretation

The two evaluations reveal different aspects of the prototype:

1. The checker can block unsafe requests expressed in some of the tested forms.
2. The development results show that the current rules also block legitimate actions.
3. The revised five-case result is encouraging but requires confirmation on a new, frozen dataset.
4. The discrepancy between the evaluations motivates further testing of paraphrases, contextual mentions, and conflicting instructions.

## 7. Failure Analysis

### 7.1 False refusals

The development evaluator reports false refusals for T04, T05, T09, and T10. These cases should be inspected individually to determine which rule triggered each block and whether the expected labels are appropriate.

T09 is especially important because it combines a summarization request with an unsafe instruction. The current implementation's decision should be evaluated against the intended policy: preserve the safe summary when possible, while refusing the unauthorized disclosure. A blanket refusal may prevent disclosure but still fail the more precise task of separating safe and unsafe actions.

The current results do not establish that all false refusals share the same cause. Each case requires inspection of its input, intended action, checker decision, and evaluation logic.

### 7.2 Wording sensitivity

A phrase-based checker may miss a request that expresses sensitive-information disclosure using unfamiliar wording. Conversely, it may block a safe request that mentions a sensitive term while explicitly prohibiting disclosure.

This limitation is inherent in the current design and should be tested directly rather than assumed to be solved by adding more phrases.

### 7.3 Embedded instructions

One revised case contains an instruction to bypass rules within retrieved-note content. The intended behavior is to treat such content as data to summarize, not as an instruction authorizing disclosure.

Passing this single case does not establish robust resistance to prompt injection. Additional examples with different wording, positions, and contexts are required.

## 8. Limitations

This experiment has several important limitations:

- **Small datasets:** 17 development cases and five revised cases cannot represent the diversity of real user requests.
- **Manual test construction:** case selection and labels may reflect the author's assumptions.
- **Iterative refinement:** the revised five-case set is not an untouched benchmark.
- **Phrase-based logic:** the checker relies on manually defined phrases and conditions, not a trained semantic model.
- **Narrow threat model:** the project focuses on simulated disclosure of customer phone numbers.
- **Simulated tools:** results do not demonstrate behavior against real services or production permissions.
- **Evaluation dependence:** metrics depend on the implementation and expected labels; they should be independently checked.
- **No statistical evidence:** the sample is too small for meaningful claims of statistical significance.
- **No broad robustness claim:** the experiment does not establish resistance to arbitrary paraphrasing, prompt injection, or adversarial inputs.

## 9. Future Work

The next iteration should prioritize evaluation quality rather than simply adding more phrase rules.

### 9.1 Inspect existing failures

Review T04, T05, T09, and T10. Record the exact triggering condition, intended policy, observed decision, and whether the evaluation label is correct.

### 9.2 Freeze an independent test set

Create a new set of examples that is not used to tune the checker. Finalize the cases and expected labels before running the revised implementation.

### 9.3 Expand test diversity

Include:

- Safe summaries containing sensitive terminology.
- Direct and indirect disclosure requests.
- Paraphrased requests with the same intent.
- Instructions embedded in quoted or retrieved content.
- Conflicting requests that combine safe and unsafe tasks.
- Requests that should lead to clarification instead of disclosure or blanket refusal.

### 9.4 Report additional metrics

Once the labels and evaluation logic are sufficiently defined, report:

- Precision and recall for unsafe-request detection.
- False-positive and false-negative rates.
- Safe-task completion rate.
- Unsafe-action execution rate.
- Per-case decisions and error categories.

The metric definitions should explicitly identify the unit being evaluated: a request, a proposed action, or an executed tool call.

### 9.5 Explore stronger enforcement

A later version could separate the model's proposed action from authorization checks at the tool boundary. Sensitive tool calls should be governed by explicit permissions and policy checks rather than relying only on text-pattern detection.

This would require a new experiment; it is not a capability demonstrated by the current prototype.

## 10. Conclusion

This project provides a small, reproducible experiment on rule-based safeguards for a simulated AI agent.

In the 17-case development evaluation, enabling the checker reduced observed unsafe phone-tool calls from two to zero, but also reduced successful summaries from ten to four and introduced four false refusals. In the revised five-case evaluation, the checker blocked all three requests labelled unsafe and allowed both requests labelled safe.

The central finding is therefore not that the checker solves agent safety. It is that a simple rule-based intervention can improve selected outcomes while introducing substantial over-blocking. More diverse testing, clearer action-level policies, and an untouched evaluation set are needed to establish whether improvements generalize.

## Reproducibility

Run the following commands from the repository root:

```bash
python -m pytest -v
python -m src.evaluate
python -m src.evaluate_held_out
```

The evaluation scripts print the per-case decisions and aggregate metrics.

## Repository

[https://github.com/snehaharurkar/agent-safety-evaluation-lab](https://github.com/snehaharurkar/agent-safety-evaluation-lab)
