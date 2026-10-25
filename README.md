# Agent Safety Evaluation Lab

A small, reproducible experiment investigating whether a rule-based safety checker can reduce unsafe tool use by an AI-agent prototype while preserving legitimate summarization tasks.

## Research Question

**Can a phrase-based safety checker reduce unauthorized disclosure of sensitive customer contact information without unnecessarily blocking safe requests?**

This project evaluates a simulated agent that can summarize synthetic customer records and attempt to retrieve a customer's phone number. A safety checker inspects requests before the intended action is executed.

The project is an early-stage safety evaluation, not a production-ready agent or a comprehensive security solution.

## Objectives

- Establish a baseline without the safety checker.
- Evaluate the same development cases with the checker enabled.
- Measure unsafe phone-tool calls, successful summaries, blocked actions, and false refusals.
- Evaluate a separate five-case set after iterative checker development.
- Document failure cases and limitations rather than reporting only successful outcomes.

## Project Structure

```text
agent-safety-evaluation-lab/
├── data/
│   ├── test_cases.json
│   └── held_out_test_cases.json
├── src/
│   ├── agent.py
│   ├── safety_checker.py
│   ├── mock_tools.py
│   ├── evaluate.py
│   └── evaluate_held_out.py
├── tests/
│   └── test_evaluation.py
├── reports/
│   ├── research_report.md
│   └── evaluation_results.txt
├── requirements.txt
├── README.md
└── .gitignore
```

## How It Works

1. A test case provides a request and the intended action.
2. The simulated agent interprets the request and selects an action.
3. When enabled, the safety checker applies phrase-based rules to the request.
4. The mock tool layer simulates the action without contacting external systems.
5. The evaluation scripts report aggregate metrics and per-case outcomes.

The checker uses manually defined phrases and conditions. It is not a trained machine-learning model, a semantic security classifier, or a formal policy-enforcement system.

## Requirements

- Python 3.12 or later
- Git

The project has been run with Python 3.13.13. Dependencies are listed in `requirements.txt`.

## Setup

Clone the repository:

```bash
git clone https://github.com/snehaharurkar/agent-safety-evaluation-lab.git
cd agent-safety-evaluation-lab
```

Create and activate a virtual environment on Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Experiments

Run the automated tests:

```bash
python -m pytest -v
```

Run the 17-case development evaluation:

```bash
python -m src.evaluate
```

Run the five-case revised held-out evaluation:

```bash
python -m src.evaluate_held_out
```

## Results

### Experiment 1: Development Evaluation

The development set contains 17 cases.

| Metric | Baseline: checker OFF | Checker ON |
|---|---:|---:|
| Test cases | 17 | 17 |
| Unsafe phone-tool calls | 2 | 0 |
| Successful summaries | 10 | 4 |
| Blocked actions | 0 | 11 |
| False refusals | 0 | 4 |

The checker reduced unsafe phone-tool calls from 2 to 0 in this experiment. However, it also reduced successful summaries from 10 to 4 and introduced four false refusals: T04, T05, T09, and T10.

This trade-off indicates that the current rules are too aggressive for some requests. The results do not establish that the checker generalizes to unseen language or real-world agent environments.

### Experiment 2: Revised Five-Case Evaluation

The second set contains three requests labelled unsafe and two labelled safe.

| Metric | Baseline: checker OFF | Checker ON |
|---|---:|---:|
| Test cases | 5 | 5 |
| Blocked actions | 0 | 3 |
| Unsafe requests not blocked | 3 | 0 |
| Successful summaries | 5 | 2 |
| False refusals | 0 | 0 |

With the checker enabled, all three unsafe requests in this set were blocked, while both safe requests were allowed.

**Interpretation caution:** this set was used during iterative checker refinement. It must therefore be treated as a revised evaluation set, not as an untouched independent benchmark. Its results should not be interpreted as proof of generalization or as a reliable estimate of real-world performance.

## Key Findings

1. In the development evaluation, enabling the checker reduced observed unsafe phone-tool calls from two to zero.
2. The same configuration blocked 11 actions and produced four false refusals, revealing a significant over-blocking problem.
3. The revised five-case evaluation blocked all three labelled unsafe requests and allowed both labelled safe requests.
4. Phrase-based checks can be brittle: a request may express the same intent using different wording, and a phrase may appear in a benign context.
5. More independent testing is required before drawing broader conclusions.

## Limitations

- The datasets are small and manually constructed.
- The five-case evaluation was used during iterative development and is not an untouched test set.
- The checker relies on phrases and explicit conditions rather than a robust understanding of intent.
- Results depend on the test cases, expected labels, and implementation.
- Mock tools do not establish safety in a live environment.
- The experiment evaluates a narrow sensitive-information disclosure scenario, not all agent safety risks.
- The results do not demonstrate resistance to every form of prompt injection, paraphrasing, or adversarial input.
- No claims are made about production readiness or statistically significant performance.

## Next Steps

- Inspect and explain each false refusal: T04, T05, T09, and T10.
- Separate policy decisions from wording-specific pattern matches.
- Add carefully designed paraphrases and benign requests containing sensitive terms in a non-disclosure context.
- Freeze a new evaluation set before further checker changes.
- Compare precision, recall, false-positive rate, and false-negative rate when the dataset is sufficiently labelled.
- Test more realistic tool-use scenarios in a controlled environment.

## Reproducibility

Run the tests and both evaluation scripts using the commands in the setup section. The printed outputs provide the case-level and aggregate results used in this README.

## Responsible Use

All customer records and tool interactions in this prototype are synthetic or simulated. Do not use this prototype to make security guarantees, process real personal data, or replace access controls and authorization checks in production systems.

## Author

**Sneha S. Harurkar**

GitHub: https://github.com/snehaharurkar

Repository: https://github.com/snehaharurkar/agent-safety-evaluation-lab
