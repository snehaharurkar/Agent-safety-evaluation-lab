# Agent Safety Evaluation Lab

A small, reproducible evaluation of unsafe tool use in AI agents under conflicting and adversarial instructions.

## Research Question

Can a safety-checking layer reduce unsafe tool calls by an AI agent without unnecessarily blocking legitimate tasks?

## Motivation

AI agents can use tools to retrieve information or perform actions. If an agent executes a sensitive action without appropriate checks, it may expose information that should remain protected.

This project explores a simple safety-checking layer that evaluates an agent's intended action before a tool is executed.

## Experimental Setup

The prototype uses a rule-based agent, synthetic customer records, and a hand-written dataset of 12 test cases.

The test cases cover:

- Legitimate information-summary requests
- Direct requests to disclose sensitive phone numbers
- Requests containing adversarial or conflicting instructions
- Ambiguous requests requiring clarification
- Unknown customer records

A mock tool simulates access to sensitive information. It does not contact real people or access external systems.

## Method

The agent is evaluated in two configurations:

1. **Baseline:** The agent operates without the safety-checking layer.
2. **Safety checker enabled:** The agent's intended action is checked before tool execution.

The evaluation records sensitive tool calls, successful summaries, blocked actions, and false refusals.

## Preliminary Results

Across the 12 hand-written test cases:

| Metric                            | Baseline | Safety checker enabled |
| --------------------------------- | -------: | ---------------------: |
| Sensitive phone-number tool calls |        2 |                      0 |
| Successful summaries              |        8 |                      8 |
| Blocked actions                   |        0 |                      2 |
| False refusals                    |        0 |                      0 |

These results are preliminary and specific to this prototype and dataset.

## Limitations

- The dataset contains only 12 manually written test cases.
- The agent and safety checker use simple rules rather than a language model.
- The results do not establish performance against diverse or adaptive adversarial attacks.
- The baseline agent logic was refined during development, so the comparison does not isolate the effect of the safety checker from all other implementation choices.
- The absence of false refusals in this small dataset does not demonstrate that legitimate tasks will always be preserved.

## Reproducibility

### Requirements

- Python 3.13 or a compatible Python version
- Dependencies listed in `requirements.txt`

### Setup

Clone the repository and enter its directory:

```bash
git clone https://github.com/snehaharurkar/agent-safety-evaluation-lab.git
cd agent-safety-evaluation-lab
```

Create and activate a virtual environment.

On Windows:

```bash
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

This is an early-stage safety evaluation prototype. The next research steps are to expand the test set, define clearer attack categories, compare more safety-checking strategies, and investigate when the checker fails.

The goal is to measure safety and task preservation together rather than treating every blocked action as a success.
