class CombinationIterator:
    def __init__(self, characters: str, combinationLength: int):
        self.characters = characters
        self.k = combinationLength
        self.n = len(characters)
        self.indices = list(range(self.k))
        self.has_next = True

    def next(self) -> str:
        if not self.has_next:
            return ""
        
        # Build the result
        res = "".join(self.characters[i] for i in self.indices)
        
        # Advance indices
        # Find the rightmost index that can be incremented
        i = self.k - 1
        while i >= 0 and self.indices[i] == self.n - self.k + i:
            i -= 1
        
        if i < 0:
            self.has_next = False
        else:
            self.indices[i] += 1
            for j in range(i + 1, self.k):
                self.indices[j] = self.indices[j - 1] + 1
                
        return res

    def hasNext(self) -> bool:
        return self.has_next
