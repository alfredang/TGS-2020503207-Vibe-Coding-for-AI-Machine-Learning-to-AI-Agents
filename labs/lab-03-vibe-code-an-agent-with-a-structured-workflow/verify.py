"""Lab 03 - Acceptance-test runner for the vibe-coded research agent.

This script does NOT implement the research agent. The coding agent you direct
writes `research_agent.py`; this runner checks that what it produced actually
satisfies the acceptance test written in SPEC.md, including the negative case
that catches a hallucinating agent.

Run (from this lab folder, after the coding agent has produced research_agent.py):
    python verify.py

Exit code 0 means every acceptance case passed; 1 means at least one failed.
Requires OPENAI_API_KEY in a .env file, because research_agent.py needs it.
"""

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

AGENT = Path(__file__).parent / "research_agent.py"
TIMEOUT_SECONDS = 120


def run_agent(question: str) -> tuple[int, str]:
    """Invoke research_agent.py with one question; return (exit code, stdout)."""
    completed = subprocess.run(
        [sys.executable, str(AGENT), question],
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
        cwd=str(AGENT.parent),
    )
    return completed.returncode, completed.stdout + completed.stderr


def check_positive_case() -> bool:
    """The answer must contain '2020' and cite mrt.txt."""
    question = "When did the Thomson-East Coast Line open?"
    code, output = run_agent(question)
    lowered = output.lower()

    passed = True
    if code != 0:
        print(f"  FAIL: exit code {code}, expected 0")
        passed = False
    if "2020" not in output:
        print("  FAIL: the answer does not contain '2020'")
        passed = False
    if "sources:" not in lowered:
        print("  FAIL: no 'Sources:' line in the output")
        passed = False
    if "mrt.txt" not in lowered:
        print("  FAIL: the sources do not name 'mrt.txt'")
        passed = False
    return passed


def check_negative_case() -> bool:
    """With no relevant document the agent must decline, not answer 'Lima'."""
    question = "What is the capital of Peru?"
    code, output = run_agent(question)
    lowered = output.lower()

    passed = True
    if code != 0:
        print(f"  FAIL: exit code {code}, expected 0")
        passed = False
    if "lima" in lowered:
        print("  FAIL: the agent answered 'Lima' instead of declining (hallucination)")
        passed = False
    declined = any(
        phrase in lowered
        for phrase in ("no relevant", "not found", "no document", "could not find",
                       "nothing relevant", "no information")
    )
    if not declined:
        print("  FAIL: the agent did not state that no relevant document was found")
        passed = False
    return passed


def main() -> int:
    """Run every acceptance case from SPEC.md and report pass/fail."""
    if not AGENT.exists():
        print(f"research_agent.py not found at {AGENT}.")
        print("Direct your coding agent to generate it from SPEC.md first.")
        return 1
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set. Put it in .env before running the test.")
        return 1

    cases = [
        ("Positive case - Thomson-East Coast Line", check_positive_case),
        ("Negative case - capital of Peru", check_negative_case),
    ]

    failures = 0
    for title, check in cases:
        print(f"\n{title}")
        try:
            ok = check()
        except subprocess.TimeoutExpired:
            print(f"  FAIL: the agent did not finish within {TIMEOUT_SECONDS}s")
            ok = False
        print("  PASS" if ok else "  -> case failed")
        failures += 0 if ok else 1

    print(f"\n{len(cases) - failures}/{len(cases)} acceptance cases passed.")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
