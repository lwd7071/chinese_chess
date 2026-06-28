import os
import sys
import subprocess
import time
from datetime import datetime

EVALS_DIR = os.path.join(".claude", "evals")
DEFINITION_FILE = os.path.join(EVALS_DIR, "project-correctness.md")
LOG_FILE = os.path.join(EVALS_DIR, "project-correctness.log")

if os.path.exists(".venv"):
    PYTHON_EXEC = os.path.join(".venv", "Scripts", "python") if os.name == "nt" else os.path.join(".venv", "bin", "python")
elif os.path.exists("venv"):
    PYTHON_EXEC = os.path.join("venv", "Scripts", "python") if os.name == "nt" else os.path.join("venv", "bin", "python")
else:
    PYTHON_EXEC = sys.executable

def run_command(args):
    try:
        res = subprocess.run(args, capture_output=True, text=True, check=True)
        return True, res.stdout + "\n" + res.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout + "\n" + e.stderr

def log_result(message):
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def main():
    if not os.path.exists(EVALS_DIR):
        os.makedirs(EVALS_DIR)

    log_result("=" * 60)
    log_result(f"EVAL RUN START: {datetime.now().isoformat()}")
    log_result("=" * 60)

    # 1. Capability: rule-validation
    log_result("Running Capability Eval: rule-validation...")
    args_rule = [PYTHON_EXEC, "-m", "unittest", "tests/test_rules.py"]
    start = time.time()
    rule_ok, rule_out = run_command(args_rule)
    rule_duration = time.time() - start
    rule_status = "PASS" if rule_ok else "FAIL"
    log_result(f"Capability [rule-validation]: {rule_status} ({rule_duration:.2f}s)")
    if not rule_ok:
        log_result(f"--- OUTPUT ---\n{rule_out}\n--------------")

    # 2. Capability: ai-level-behavior
    log_result("Running Capability Eval: ai-level-behavior...")
    args_ai = [PYTHON_EXEC, "-m", "unittest", "tests/test_ai_level1.py", "tests/test_ai_level3.py", "tests/test_ai_level4.py", "tests/test_ai_level6.py"]
    start = time.time()
    ai_ok, ai_out = run_command(args_ai)
    ai_duration = time.time() - start
    ai_status = "PASS" if ai_ok else "FAIL"
    log_result(f"Capability [ai-level-behavior]: {ai_status} ({ai_duration:.2f}s)")
    if not ai_ok:
        log_result(f"--- OUTPUT ---\n{ai_out}\n--------------")

    # 3. Regression: thread-safety (Stability run: 3 trials to compute pass^3)
    log_result("Running Regression Eval: thread-safety (pass^3 stability check)...")
    args_thread = [PYTHON_EXEC, "-m", "unittest", "tests/test_main_thread_safety.py"]
    thread_results = []
    
    for i in range(1, 4):
        log_result(f"  Trial {i}/3...")
        start = time.time()
        ok, out = run_command(args_thread)
        duration = time.time() - start
        thread_results.append(ok)
        log_result(f"    Trial {i}: {'PASS' if ok else 'FAIL'} ({duration:.2f}s)")
        if not ok:
            log_result(f"--- OUTPUT ---\n{out}\n--------------")

    thread_ok = all(thread_results)
    thread_status = "PASS" if thread_ok else "FAIL"
    pass_cubed = sum(1 for r in thread_results if r) / 3.0
    log_result(f"Regression [thread-safety]: {thread_status} (pass^3 = {pass_cubed:.2%})")

    # Report Summary
    log_result("=" * 60)
    log_result("EVAL SUMMARY REPORT")
    log_result("=" * 60)
    log_result(f"Capability [rule-validation]:   {rule_status}")
    log_result(f"Capability [ai-level-behavior]: {ai_status}")
    log_result(f"Regression [thread-safety]:     {thread_status} (pass^3 = {pass_cubed:.2%})")
    
    total_passed = sum([1 if rule_ok else 0, 1 if ai_ok else 0, 1 if thread_ok else 0])
    log_result(f"Overall Status: {total_passed}/3 passed")
    log_result(f"EVAL RUN END: {datetime.now().isoformat()}")
    log_result("=" * 60 + "\n")

    if total_passed == 3:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
