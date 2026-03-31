from typing import List

class Solution:
    def videoStitching(self, clips: List[List[int]], time: int) -> int:
        clips.sort()
        res = 0
        cur_end, next_end, i = 0, 0, 0
        n = len(clips)
        while cur_end < time:
            while i < n and clips[i][0] <= cur_end:
                next_end = max(next_end, clips[i][1])
                i += 1
            if cur_end == next_end:
                return -1
            res += 1
            cur_end = next_end
        return res
