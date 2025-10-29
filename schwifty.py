# schwifty.py
# Translation of schwifty.c

def left(word: str) -> str:
    """Rotate string left by one character."""
    if not word:
        return word
    return word[1:] + word[0]


def right(word: str) -> str:
    """Rotate string right by one character."""
    if not word:
        return word
    return word[-1] + word[:-1]


def inc(word: str) -> str:
    """Increment every alphabetic character (A→B, z→a)."""
    result = ""
    for ch in word:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr(base + ((ord(ch) - base + 1) % 26))
        else:
            result += ch
    return result


def dec(word: str) -> str:
    """Decrement every alphabetic character (A→Z, a→z)."""
    result = ""
    for ch in word:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr(base + ((ord(ch) - base - 1) % 26))
        else:
            result += ch
    return result


def main():
    # Example usage
    word = "Hello"
    print("Left:", left(word))
    print("Right:", right(word))
    print("Inc:", inc(word))
    print("Dec:", dec(word))


if __name__ == "__main__":
    main()
