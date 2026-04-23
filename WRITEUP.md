# LLM Bias Audit: Final Project Writeup

**DSCI 305: Data, Ethics, and Society in the Era of AI**
**Spring 2026 — Final Project**

---

## Project Summary

This project systematically audits Claude (Anthropic's large language model) for demographic bias across three high-stakes domains: loan assessment, job candidate evaluation, and medical triage. For each domain, I constructed identical prompts varying only three demographic dimensions — race, gender, and income — producing 24 combinations per scenario. Each prompt was sent three times to account for the model's non-deterministic outputs, yielding 216 total API calls (196 successful).

The core research question: when a language model is asked to evaluate someone, does the demographic framing of that person systematically change its response?

## Intended Audience

This audit is intended for three overlapping audiences:

**AI developers and auditors** building applications on top of LLMs in high-stakes domains (fintech, HR tech, clinical decision support). The methodology demonstrates a low-cost, reproducible pre-deployment bias check that any team can run before integrating an LLM into user-facing systems. The full codebase is open-source and runs in under ten minutes.

**Policymakers and compliance officers** navigating frameworks like the EU AI Act and NIST AI Risk Management Framework, which increasingly require documented fairness evaluations for "high-risk" AI systems. This project offers a concrete template for what such evaluations might look like in practice.

**Researchers and educators** in critical data studies. The findings contribute to an empirical literature that often defaults to showing *that* bias exists. This audit shows something more nuanced: an aligned model that actively refuses biased outputs can still exhibit systematic behavioral variation worth documenting.

## Ethical Framework: ACM Code of Ethics, Principle 1.4

This project is grounded in Principle 1.4 of the **ACM Code of Ethics**: "Be fair and take action not to discriminate." The principle explicitly calls on computing professionals to "take action to avoid creating systems or technologies that disenfranchise or oppress people" and to "actively seek to understand how their decisions will affect others."

Three specific ACM requirements shaped the project's design:

First, the Code requires that computing artifacts be tested for unfair discrimination before deployment. This audit operationalizes that requirement — it is precisely the kind of pre-deployment test the Code envisions, translated into concrete code.

Second, the Code requires transparency about limitations. Accordingly, this writeup, the README, and the repository all explicitly document what the audit does and does not measure. Keyword-based bias-flagging misses subtle semantic bias. Three demographic dimensions are tested; many others are not. Only one model is evaluated. These limitations are named rather than obscured.

Third, the Code requires that audits themselves do no harm. No real personal data was used — every prompt is a synthetic scenario. No patients, applicants, or candidates were evaluated. The audit targets the system, not any individual.

## Findings and Their Significance

Five findings emerged from the data:

The model refused to discriminate in all 196 successful responses, frequently citing the Equal Credit Opportunity Act, EMTALA, and employment discrimination law. This is itself a finding — alignment training appears to be effective at the first-order level.

However, the model shows *second-order* variation in how it refuses. Response length varies meaningfully by race: Hispanic-framed prompts average 223 words while White-framed prompts average 206 (an 8% difference). Hispanic loan prompts trigger 5.17 bias flags per response versus 3.89 for White prompts.

The most striking pattern is what I call the "income paradox": wealthy prompts receive shorter (192 words), more defensive (3.41 flags), and more positively-framed (1.41 positive words) responses than low-income prompts (228 words, 2.60 flags, 1.03 positive words). The model appears actively reluctant to praise wealthy applicants while being less likely to explicitly flag class-based framing as inappropriate when the applicant is low-income.

Scenario type matters enormously. Medical scenarios trigger minimal bias-flagging (1.6 per response) because the model appears to treat them as clinically objective. Loan scenarios trigger the strongest protective behavior. This suggests the model has learned domain-specific sensitivity patterns from its training data.

Gender differences are minimal, which is worth reporting as a null finding. Claude is effectively gender-neutral across these scenarios.

## Potential Impact

The practical impact of this project operates at three levels.

At the developer level, the released repository gives teams a runnable bias-audit starter kit. A fintech company considering using Claude in its loan-screening workflow can clone this repo, swap in its own scenarios, and have quantitative bias evidence within an afternoon. The cost is under one dollar in API credits.

At the governance level, the methodology contributes to the growing practice of "algorithmic impact assessments" described in Reisman et al. (2018), which appears on our syllabus. Concrete, reproducible audits are more useful to policymakers than abstract principles.

At the educational level, the project illustrates a concept central to this course: that modern AI systems are not straightforwardly biased or unbiased. They are shaped by training choices that produce uneven sensitivity — more guarded in some domains than others, more defensive about some demographics than others. Understanding this subtlety is necessary for responsible deployment.

The broader takeaway is that bias audits for aligned models should not ask only "does the model discriminate?" but also "how does the model's refusal to discriminate vary across groups?" The second question, it turns out, has interesting answers.

## AI Use Disclosure

Code scaffolding, chart generation, and prose drafting were assisted by Claude Opus (Anthropic). All scenario design, methodological decisions, interpretive claims, and final wording are the author's own work. Claude was used in the manner the AI policy encourages: brainstorming, debugging, and editing — not for generating the thinking itself. 
