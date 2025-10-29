# e3q2.py
import sys

def verify(args):
    """Return True if valid, False if invalid.
       - 4 arguments total (script + 3 numbers)
       - size > 0
       - start > 0
       - inc <= start
    """
    if len(args) != 4:
        return False
    try:
        size = int(args[1])
        start = int(args[2])
        inc = int(args[3])
    except ValueError:
        return False

    if size <= 0 or start <= 0 or inc > start:
        return False
    return True


def build_array(size, start, inc):
    """Return list of given size starting at 'start' and incremented by 'inc'."""
    return [start + (i * inc) for i in range(size)]


def main():
    if not verify(sys.argv):
        print("Invalid arguments")
        sys.exit(1)

    size = int(sys.argv[1])
    start = int(sys.argv[2])
    inc = int(sys.argv[3])

    arr = build_array(size, start, inc)
    print(" ".join(map(str, arr)))


if __name__ == "__main__":
    main()
