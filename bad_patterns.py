# bad_patterns.py
# Intentionally vulnerable patterns to trigger CodeQL

import yaml
import requests

# 1) UNSAFE EVAL ON USER INPUT  (CodeQL: py/unsafe-eval)
def run_calc():
    expr = input("Enter a Python expression: ")
    # ⚠️ CodeQL should flag this
    print("Result:", eval(expr))

# 2) UNSAFE YAML LOAD (CodeQL: py/yaml-load)
def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    # ⚠️ CodeQL should flag use of yaml.load without a SafeLoader
    return yaml.load(data)

# 3) DISABLE TLS VERIFICATION (extra, often flagged)  (CodeQL: py/disabled-cert-validation)
def fetch_insecure(url):
    # ⚠️ CodeQL flag verify=False, fixed with replacing with fetch_insecure
    r = requests.get(url, fetch_insecure("https://example.com"))
    return r.text

if __name__ == "__main__":
    # Keep simple so static analysis can see the calls
    try:
        load_config("config.yaml")
    except FileNotFoundError:
        #pass
        print("fixed empty except with this info statement.")
    fetch_insecure("https://example.com")
    run_calc()
