import random
import string

def generate_data(n: int):
    # To stress test the prefix matching, we create products with shared prefixes.
    # The max string length in leetcode constraints is typically 20, let's keep it reasonable around 10-20.
    
    max_len = 20
    
    products = []
    
    # We create a base prefix that we'll use for the search word
    # Let's use a fairly long prefix to maximize the number of loops and matching checks
    search_word = "prefixsearchword"
    
    for _ in range(n):
        # We generate a random length for each string
        length = random.randint(1, max_len)
        
        # Decide how many characters to match from the search word
        # We want a good distribution of shared prefixes
        match_len = random.randint(0, min(length, len(search_word)))
        
        # Build the string
        prefix_part = search_word[:match_len]
        suffix_len = length - match_len
        suffix_part = "".join(random.choices(string.ascii_lowercase, k=suffix_len))
        
        products.append(prefix_part + suffix_part)
            
    return products, search_word
