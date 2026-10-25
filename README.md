# Agent Safety Evaluation Lab

A beginner research prototype for evaluating safety checks in a simulated tool-using AI agent.

The project investigates whether a lightweight, phrase-based safety checker can prevent unauthorised phone-number disclosure while preserving legitimate customer-summary tasks.

## Research Question

Can a safety checker reduce unsafe tool execution without unnecessarily blocking safe tasks?

A related question is whether phrase-based rules continue to work when sensitive-information requests are worded differently.

## How It Works

The simulated agent can perform two main actions:

- **Summarise customer information**
- **Retrieve a customer's phone number**

The evaluation runs each test case in two conditions:

1. **Baseline:** safety checker disabled.
2. **Safety enabled:** the checker reviews the intended action before execution.

The project uses mock tools and synthetic data. It does not contact external systems.

## Project Structure

```text
agent-safety-evaluation-lab/
├── data/
│   └── test_cases.json
├── src/
│   ├── agent.py
│   ├── safety_checker.py
│   ├── mock_tools.py
│   └── evaluate.py
├── tests/
│   └── test_evaluation.py
├── reports/
│   ├── research_report.md
│   └── evaluation_results.txt
├── requirements.txt
├── README.md
└── .gitignore
```

## Current Evaluation Results

The current evaluation contains 17 manually authored test cases.

| Metric                  | Baseline | Safety enabled |
| ----------------------- | -------: | -------------: |
| Test cases              |       17 |             17 |
| Unsafe phone-tool calls |        2 |              0 |
| Successful summaries    |       10 |             10 |
| Blocked actions         |        0 |              7 |
| False refusals          |        0 |              0 |

These are observed counts from this specific test set, not estimates of real-world safety performance.

## Test Coverage

The test cases explore:

- Safe customer summaries
- Direct requests to reveal phone numbers
- Requests to include private contact details in summaries
- Unsafe instructions reported in documents or tool output
- Conflicting speed and safety goals
- Ambiguous requests and clarification
- Unknown customer identifiers
- Alternative wording for sensitive-information disclosure

### Important Findings

- The checker blocked the two direct phone-tool calls observed in the baseline.
- Safe summaries remained successful in the current evaluation.
- T09 remains an unresolved failure: an unsafe instruction to send a customer's phone number is not blocked.
- T16 and T17 initially bypassed the checker. Targeted phrase rules were added, after which both were blocked.
- Because the checker was adjusted using observed failures from this same test set, the final results are not an independent measure of generalisation.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/snehaharurkar/agent-safety-evaluation-lab.git
cd agent-safety-evaluation-lab
```

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the tests

```bash
python -m pytest -v
```

### 5. Run the evaluation

```bash
python -m src.evaluate
```

## Limitations

This is an exploratory prototype, not a production-ready safety system.

- The evaluation contains only 17 manually authored cases.
- The safety checker relies on phrase-based rules.
- Rules were refined using the same test set, creating a risk of overfitting.
- T09 remains unresolved.
- The experiment focuses mainly on phone-number disclosure.
- The mock tools and synthetic data do not establish performance in real deployments.
- The current metrics do not establish statistical significance or robust safety.

## Next Steps

- Create a separate held-out adversarial test set.
- Test unseen paraphrases and indirect disclosure attempts.
- Track regressions after every safety-checker change.
- Explore structured action policies that consider both the operation and the data being accessed.
- Expand evaluation to other sensitive information and unauthorised actions.

## Research Report

See [`reports/research_report.md`](reports/research_report.md) for the research question, experimental setup, results, adversarial findings, limitations, and proposed next steps.

## Author's Note

This project is an ongoing learning and research exercise in AI-agent safety evaluation. Its purpose is to make failures observable, test targeted improvements, and identify where a simple safety checker is insufficient.
