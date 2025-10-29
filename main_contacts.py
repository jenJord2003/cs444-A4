# main_contacts.py
# Translation of main.c (ContactNode linked list)

class ContactNode:
    def __init__(self, name: str, phone: str):
        self.contact_name = name
        self.contact_phone_num = phone
        self.next_contact_node = None


def insert_after(contact_node, new_contact_node):
    new_contact_node.next_contact_node = contact_node.next_contact_node
    contact_node.next_contact_node = new_contact_node


def mask_phone(phone):
    """Mask all but the last 2 digits of a phone number."""
    if not phone or len(phone) <= 2:
        return '*' * len(phone)
    num_mask = '*' * (len(phone) - 2) + phone[-2:]
    return num_mask


def print_contact_node(contact_node):
    print(f"Name: {contact_node.contact_name}")
    print(f"Phone number: {mask_phone(contact_node.contact_phone_num)}")


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
        print(f"Person {i}: {c.contact_name}, {mask_phone(c.contact_phone_num)}")

    print("\nCONTACT LIST")
    current = contacts[0]
    while current:
        print_contact_node(current)
        print()
        current = current.next_contact_node


if __name__ == "__main__":
    main()
