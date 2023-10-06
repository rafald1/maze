class Stack:
    """Used in both DFS to push element to the stack and to pop the last element."""
    def __init__(self):
        self.items = []

    def is_empty(self):
        return not self.items

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def peak(self, index):
        return self.items[index]

    def __str__(self):
        return str(self.items)
