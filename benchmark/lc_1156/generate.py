import random
import string

def generate_data(n: int) -> str:
    """
    Generates synthetic strings of length `n`.
    Mixes random characters with long repeated blocks of characters to
    thoroughly stress-test the algorithm, particularly strings where
    group merging might occur.
    """
    if n <= 0:
        return ""

    chars = []
    current_len = 0
    while current_len < n:
        # Decide whether to add a single random character or a block
        if random.random() < 0.2:
            # Add a single random char
            chars.append(random.choice(string.ascii_lowercase))
            current_len += 1
        else:
            # Add a block of repeated characters
            # The block length is up to max(10, n // 10)
            max_block = max(1, n // 10)
            block_len = random.randint(1, min(max_block, n - current_len))
            c = random.choice(string.ascii_lowercase)
            chars.append(c * block_len)
            current_len += block_len
            
    return "".join(chars)[:n]
