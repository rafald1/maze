class Queue:
    """Used in BFS to enqueue element to the queue and to dequeue the last element."""
    def __init__(self):
        self.items = []

    def is_empty(self):
        return not self.items

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

    def peak(self, index):
        return self.items[index]

    def __str__(self):
        return str(self.items)
