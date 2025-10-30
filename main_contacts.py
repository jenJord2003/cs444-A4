# main_contacts.py
# Translation of main.c (ContactNode linked list)



class ContactNode:
    def __init__(self, name: str, phone: str):
        self.contact_name = name
        self.contact_phone_num = phone
        self.next_contact_node = None

def mask_phone(num: str, keep_last: int = 4) -> str:
    # keeps last N digits; masks the rest (leaves non-digits as-is)
    digits = [c for c in num if c.isdigit()]
    if len(digits) <= keep_last:
        return "*" * max(0, len(digits) - 1) + (digits[-1] if digits else "")
    masked = "*" * (len(digits) - keep_last) + "".join(digits[-keep_last:])
    # reinsert punctuation roughly (simple approach)
    out = []
    d_i = 0
    for c in num:
        if c.isdigit():
            out.append(masked[d_i])
            d_i += 1
        else:
            out.append(c)
    return "".join(out)


def insert_after(contact_node, new_contact_node):
    new_contact_node.next_contact_node = contact_node.next_contact_node
    contact_node.next_contact_node = new_contact_node

def print_contact_node(contact_node):
    print(f"Name: {contact_node.contact_name}")

def main():
    contacts = []

    for i in range(3):
        name = input(f"Enter name of person {i+1}: ").strip()
        phone = input(f"Enter phone number of person {i+1}: ").strip()
        contacts.append(ContactNode(name, phone))

    # Link them together
    for i in range(len(contacts) - 1):
        insert_after(contacts[i], contacts[i + 1])

    print("\nPerson list:")
    for i, c in enumerate(contacts, start=1):
        print(f"Person {i}: {c.contact_name}")


    print("\nCONTACT LIST")
    current = contacts[0]
    while current:
        print_contact_node(current)
        print()
        current = current.next_contact_node


if __name__ == "__main__":
    main()
