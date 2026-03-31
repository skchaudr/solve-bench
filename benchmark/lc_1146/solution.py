import bisect

class SnapshotArray:
    def __init__(self, length: int):
        self.current_snap = 0
        self.history = [[[-1, 0]] for _ in range(length)]

    def set(self, index: int, val: int) -> None:
        if self.history[index][-1][0] == self.current_snap:
            self.history[index][-1][1] = val
        else:
            self.history[index].append([self.current_snap, val])

    def snap(self) -> int:
        self.current_snap += 1
        return self.current_snap - 1

    def get(self, index: int, snap_id: int) -> int:
        idx = bisect.bisect_right(self.history[index], [snap_id, float('inf')])
        return self.history[index][idx - 1][1]
