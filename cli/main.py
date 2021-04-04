from dataclasses import dataclass, field

from lib import HashTableProtocol


@dataclass
class MainActivity:
    hash_table: HashTableProtocol

    _running: bool = field(default=True, init=False)

    def start(self):
        self._running = True

        selector = {
            "1": self._add_value,
            "2": self._get_value,
            "3": self._exit,
        }

        while self._running:
            print("Select action:")
            print("1. Add value")
            print("2. Get value")
            print("3. Exit")
            print(">> ", end="")

            user_choice = selector.get(input())

            if user_choice is None:
                print("No such option\n")
            else:
                user_choice()

    def _add_value(self):
        key = input("Enter key: ")
        value = input("Enter value: ")

        self.hash_table.add(key, value)
        print("Added!\n")

    def _get_value(self):
        key = input("Enter key: ")

        result = self.hash_table.get(key)

        if result is None:
            print("Value with such key not found")
        else:
            index, value = result
            print("Found value!")
            print(f"Index: {index}")
            print(f"{value}\n")

    def _exit(self):
        self._running = False
