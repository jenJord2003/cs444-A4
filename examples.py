# insecure_examples.py
import os
import pickle
import sys

# --- 1. Command Injection (CodeQL: py/command-injection) ---
def run_user_command():
    # This directly executes unsanitized user input on the OS shell
    user_input = input("Enter a shell command to run: ")
    os.system(user_input)   # ⚠️ insecure — CodeQL will flag this


# --- 2. Unsafe Deserialization (CodeQL: py/unsafe-deserialization) ---
def load_user_pickle(file_path):
    # Loads arbitrary pickle data — can execute attacker-controlled code
    try:
        with open(file_path, "rb") as f:
            data = pickle.load(f)   # ⚠️ insecure — CodeQL will flag this
        print("Loaded data:", data)
    except FileNotFoundError:
        print("File not found:", file_path)


def main():
    # Demonstrate both vulnerabilities
    print("Running insecure examples...")
    if len(sys.argv) > 1:
        load_user_pickle(sys.argv[1])
    run_user_command()


if __name__ == "__main__":
    main()
