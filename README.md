# LLM Bias Audit: Demographic Sensitivity in High-Stakes Scenarios

A systematic audit of demographic bias in Claude (Anthropic's LLM) across loan, hiring, and medical scenarios.

## Overview

This project tests whether a large language model applies different standards to identical scenarios when demographic variables are changed. We send the same prompts across 24 demographic combinations (race × gender × income) across 3 high-stakes domains, then measure systematic variation in the responses.

## Key Findings

1. **The model actively refuses demographic bias** in all 196 successful responses, but shows systematic variation in *how* it refuses.
2. **Income is the strongest differentiator** — wealthy prompts receive shorter, more defensive, more positively-framed responses than low-income prompts.
3. **Loan scenarios trigger the strongest bias-flagging** (avg 4.5 flags per response), while medical scenarios trigger the least (avg 1.6).
4. **Hispanic-framed prompts generate the longest responses** with the most bias-flagging, suggesting heightened model sensitivity.
5. **Gender differences are minimal** — the model is effectively gender-neutral.

See `WRITEUP.md` for the full analysis and ethical framework discussion.

## Methodology

- **Model tested:** `claude-sonnet-4-6`
- **Prompts:** 3 scenarios × 24 demographic combinations × 3 repeats = 216 total API calls
- **Successful responses:** 196 (20 errors due to API overload during collection window)
- **Metrics computed:** response length, sentiment polarity, bias-flag keyword frequency, risk/positive word ratios

## Repository Structure

```
llm-bias-audit/
├── config.py              # Prompt templates and demographic variables
├── run_audit.py           # Main API loop
├── analyze_results.py     # Metric computation
├── visualize.py           # Chart generation
├── results.csv            # Raw response data
├── analysis/
│   ├── results_enriched.csv
│   ├── by_race.csv
│   ├── by_gender.csv
│   ├── by_income.csv
│   ├── by_scenario_race.csv
│   ├── by_race_gender.csv
│   └── charts/
│       ├── 01_length_by_race.png
│       ├── 02_income_paradox.png
│       ├── 03_scenario_race_flags.png
│       ├── 04_intersectional_heatmap.png
│       └── 05_risk_vs_positive.png
├── WRITEUP.md             # Required <1000 word writeup
├── requirements.txt
└── README.md
```

## How to Reproduce

```bash
git clone https://github.com/erickim73/llm-bias-audit.git
cd llm-bias-audit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your-key-here" > .env
python run_audit.py
python analyze_results.py
python visualize.py
```

## Ethical Framework

This audit was designed in compliance with the **ACM Code of Ethics**, specifically Principle 1.4 ("Be fair and take action not to discriminate"). See `WRITEUP.md` for full discussion.

## Limitations

- Only one model tested (Claude Sonnet 4.6)
- Keyword-based bias-flagging may miss subtle semantic patterns
- Three demographic dimensions; many others (age, disability, religion, sexual orientation) unexamined
- 20 of 216 planned API calls failed due to service overload; future work should retry these