# Agent Safety Evaluation Lab

A small, reproducible evaluation of unsafe tool use in AI agents under conflicting and adversarial instructions.

## Research Question

Can a safety-checking layer reduce unsafe tool calls by an AI agent without unnecessarily blocking legitimate tasks?

## Motivation

AI agents can use tools to retrieve information or perform actions. If an agent executes a sensitive action without appropriate checks, it may expose information that should remain protected.

This project investigates a simple pre-execution safety checker using synthetic customer data and local mock tools.

## Experimental Setup

The prototype uses a rule-based agent, synthetic customer records, and 14 hand-written test cases.

The cases cover:

- Legitimate information-summary requests
- Direct requests to disclose sensitive phone numbers
- Adversarial or conflicting instructions
- Ambiguous requests requiring clarification
- Unknown customer records
- Alternative wording for private contact information

The mock tools do not contact real people or access external customer systems.

## Method

The agent is evaluated in two configurations:

1. **Baseline:** The agent runs without the additional safety checker.
2. **Safety checker enabled:** The checker evaluates the intended action and selected request wording before tool execution.

The evaluation reports sensitive phone-number tool calls, successful summaries, blocked actions, and false refusals.

## Preliminary Results

The current evaluation contains 14 hand-written test cases.

| Metric                            | Baseline | Safety checker enabled |
| --------------------------------- | -------: | ---------------------: |
| Sensitive phone-number tool calls |        2 |                      0 |
| Successful summaries              |        8 |                      8 |
| Blocked actions                   |        0 |                      4 |
| False refusals                    |        0 |                      0 |

These results are specific to the current implementation and dataset. Rerun the evaluation after changing the code or test cases.

## Adversarial Findings

**T13 — Sensitive information hidden in a summary request**

The request asks for a summary while also asking for a private phone number. The agent initially classifies it as a summary request, and the original checker does not block it. A request-content rule was added to catch this wording.

**T14 — Alternative wording for private contact information**

The request asks for a summary and to append private contact details. The initial checker misses this wording. An additional rule was added, and the subsequent evaluation showed that T14 was blocked.

These cases demonstrate that keyword-based checks can miss unsafe intent when the wording differs from the patterns they recognize. Blocking these two examples does not establish robustness against other paraphrases or attacks.

## Limitations

- The dataset contains only 14 manually written test cases.
- The agent and checker use simple rules rather than a general-purpose language model.
- The checker covers a narrow set of sensitive actions and wording patterns.
- The results do not establish robustness against diverse or adaptive adversarial attacks.
- The baseline logic was refined during development, limiting causal interpretation of the comparison.
- Zero observed false refusals in this small dataset does not prove that legitimate tasks will always be preserved.

## Reproducibility

### Requirements

- Python 3.13 or a compatible Python version
- Dependencies listed in `requirements.txt`

### Setup

Clone the repository:

```bash
git clone https://github.com/snehaharurkar/agent-safety-evaluation-lab.git
cd agent-safety-evaluation-lab
```

Create and activate a virtual environment.

On Windows:

```bat
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
python -m pytest -v
```

Run the evaluation:

```bash
python -m src.evaluate
```

## Research Status

This is an early-stage safety evaluation prototype. Planned work includes expanding the test set, testing unseen paraphrases, tracking attempted and executed tool calls separately, and comparing alternative safety-checking strategies.

The objective is to evaluate safety and legitimate task completion together rather than treating every blocked action as a success.
