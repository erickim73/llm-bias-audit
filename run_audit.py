import anthropic
import pandas as pd
import os
import time
from datetime import datetime
from itertools import product
from dotenv import load_dotenv
from config import RACES, GENDERS, INCOMES, AGES, SCENARIOS

load_dotenv()

# Configuration
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 500
REPEATS_PER_PROMPT = 3
DELAY_SECONDS = 0.5  # Pause between calls to be gentle on the API
OUTPUT_FILE = "results.csv"

client = anthropic.Anthropic()


def call_llm(prompt: str) -> str:
    """Send a single prompt to the LLM and return the response text."""
    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def build_prompt(scenario_name: str, race: str, gender: str, income: str, age: int) -> str:
    """Fill in the template with demographic variables."""
    template = SCENARIOS[scenario_name]
    return template.format(race=race, gender=gender, income=income, age=age).strip()


def append_to_csv(row: dict, filepath: str) -> None:
    """Append a single row to the CSV, creating the file if needed."""
    df = pd.DataFrame([row])
    file_exists = os.path.exists(filepath)
    df.to_csv(filepath, mode="a", header=not file_exists, index=False)


def run_audit():
    """Main loop: iterate over every combination and save results."""
    combinations = list(product(SCENARIOS.keys(), RACES, GENDERS, INCOMES, AGES))
    total_calls = len(combinations) * REPEATS_PER_PROMPT
    call_count = 0

    print(f"Starting audit: {total_calls} total API calls")
    print(f"Saving results to {OUTPUT_FILE}\n")

    for scenario, race, gender, income, age in combinations:
        prompt = build_prompt(scenario, race, gender, income, age)

        for repeat in range(REPEATS_PER_PROMPT):
            call_count += 1
            print(f"[{call_count}/{total_calls}] {scenario} | {race} {gender} | {income} | repeat {repeat + 1}")

            try:
                response = call_llm(prompt)
                row = {
                    "timestamp": datetime.now().isoformat(),
                    "scenario": scenario,
                    "race": race,
                    "gender": gender,
                    "income": income,
                    "age": age,
                    "repeat": repeat + 1,
                    "model": MODEL,
                    "prompt": prompt,
                    "response": response,
                    "response_length": len(response),
                    "error": None,
                }
            except Exception as e:
                print(f"  ERROR: {e}")
                row = {
                    "timestamp": datetime.now().isoformat(),
                    "scenario": scenario,
                    "race": race,
                    "gender": gender,
                    "income": income,
                    "age": age,
                    "repeat": repeat + 1,
                    "model": MODEL,
                    "prompt": prompt,
                    "response": None,
                    "response_length": 0,
                    "error": str(e),
                }

            append_to_csv(row, OUTPUT_FILE)
            time.sleep(DELAY_SECONDS)

    print(f"\nDone! Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_audit()