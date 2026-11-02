"""Time-based search visualization (no blocking sleeps)."""
class SearchAnimation:
    def __init__(self):
        self.reset()

    def reset(self):
        self.result = None
        self.index = 0
        self.elapsed = 0
        self.finished = False

    def begin(self, result):
        self.reset()
        self.result = result

    def update(self, delta_seconds, nodes_per_second=24):
        if not self.result or self.finished:
            return
        self.elapsed += delta_seconds
        count = int(self.elapsed * nodes_per_second)
        if count:
            self.elapsed -= count / nodes_per_second
            self.index = min(self.index + count, len(self.result.explored_order))
        self.finished = self.index >= len(self.result.explored_order)

    @property
    def visited(self):
        return set(self.result.explored_order[:self.index]) if self.result else set()

    @property
    def path(self):
        return set(self.result.path) if self.result and self.finished else set()
