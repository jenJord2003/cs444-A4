# caps.py
import sys

def caps(s):
    """Recursively count capital letters."""
    if s == "":
        return 0
    return (1 if s[0].isupper() else 0) + caps(s[1:])


def main():
    if len(sys.argv) != 2:
        print("Usage: python caps.py <string>")
        sys.exit(1)
    word = sys.argv[1]
    print(f"{word} has {caps(word)} capital letters")


if __name__ == "__main__":
    main()
