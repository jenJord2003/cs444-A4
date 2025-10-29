# linked_list_names.py
# Translation of one.c

class Node:
    def __init__(self, name: str):
        self.name = name
        self.next = None


def add_back(head: Node, name: str) -> Node:
    node = Node(name)
    if head is None:
        return node
    cur = head
    while cur.next:
        cur = cur.next
    cur.next = node
    return head


def print_list(head: Node):
    cur = head
    while cur:
        print(cur.name)
        cur = cur.next


def main():
    head = None
    print('Enter strings to add to the list, "STOP" to end:')
    while True:
        name = input().strip()
        if name.upper() == "STOP":
            break
        head = add_back(head, name)

    print("\nSublist:")
    print_list(head)


if __name__ == "__main__":
    main()
