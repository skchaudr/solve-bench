from typing import List

class Solution:
    def avoidFlood(self, rains: List[int]) -> List[int]:
        import bisect
        ans = [-1] * len(rains)
        dry_days = []
        full_lakes = {}
        
        for i, lake in enumerate(rains):
            if lake == 0:
                dry_days.append(i)
                ans[i] = 1 # default to 1
            else:
                if lake in full_lakes:
                    # Need to dry this lake before today
                    prev_rain_day = full_lakes[lake]
                    # Find a dry day strictly after prev_rain_day
                    idx = bisect.bisect_right(dry_days, prev_rain_day)
                    if idx < len(dry_days):
                        dry_day = dry_days.pop(idx)
                        ans[dry_day] = lake
                    else:
                        return []
                full_lakes[lake] = i
        return ans
