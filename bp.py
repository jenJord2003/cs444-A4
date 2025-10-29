# bp.py
class Letter:
    def __init__(self, ch):
        self.info = ch
        self.next = None


def add_front(head, ch):
    """Optional helper to insert at front (not required)."""
    node = Letter(ch)
    node.next = head
    return node


def build_list(word: str):
    """Build a linked list representing the word."""
    head = None
    tail = None
    for ch in word:
        node = Letter(ch)
        if head is None:
            head = tail = node
        else:
            tail.next = node
            tail = node
    return head


def print_list(head):
    """Print linked list: e.g. C-->R-->I-->M-->S-->O-->N"""
    cur = head
    parts = []
    while cur:
        parts.append(cur.info)
        cur = cur.next
    print("-->".join(parts))


def main():
    word = input("Enter a word: ").strip()
    head = build_list(word)
    print_list(head)


if __name__ == "__main__":
    main()
