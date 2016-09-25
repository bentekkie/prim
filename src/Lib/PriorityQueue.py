class PriorityQueue:

    def __init__(self):
        self._values = []
        self._first = None
        return

    def is_empty(self):
        return len(self._values) == 0

    def __len__(self):
        return len(self._values)

    def insert(self, value):
        self._values.append(value)
        if self._first == None:
            self._first = 0
        elif value < self._values[self._first]:
            self._first = len(self._values) - 1
        return

    def remove(self):
        assert len(
            self._values) > 0, "Cannot remove from an empty priority queue"

        value = self._values.pop(self._first)
        if len(self._values) > 0:
            self._first = 0
            for x in range(len(self._values)):
                if self._values[x] < self._values[self._first]:
                    self._first = x
        else:
            self._first = None

        return value

    def peek(self):

        return self._values[self._first]

    def __str__(self):
        return "[" + ",".join(str(x) for x in self._values) + "]"
