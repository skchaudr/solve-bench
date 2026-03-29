import json
import random
import os

def generate_valid_tree(n):
    leftChild = [-1] * n
    rightChild = [-1] * n
    
    nodes = list(range(n))
    random.shuffle(nodes)
    
    root = nodes[0]
    available = [root]
    
    for i in range(1, n):
        # Pick a random parent that has available slots
        idx = random.randrange(len(available))
        parent = available[idx]
        child = nodes[i]
        
        # Assign to left or right
        if leftChild[parent] == -1 and rightChild[parent] == -1:
            if random.random() < 0.5:
                leftChild[parent] = child
            else:
                rightChild[parent] = child
        elif leftChild[parent] == -1:
            leftChild[parent] = child
        else:
            rightChild[parent] = child
            
        # If parent is now full, remove from available
        if leftChild[parent] != -1 and rightChild[parent] != -1:
            available[idx] = available[-1]
            available.pop()
            
        available.append(child)
                
    return leftChild, rightChild

def generate_invalid_tree(n):
    leftChild, rightChild = generate_valid_tree(n)
    
    if n > 2:
        # Introduce multiple parents or cycle
        node1 = random.randrange(n)
        node2 = random.randrange(n)
        while node1 == node2:
            node2 = random.randrange(n)
            
        if leftChild[node1] == -1:
            leftChild[node1] = node2
        elif rightChild[node1] == -1:
            rightChild[node1] = node2
        else:
            leftChild[node1] = node2
            
    return leftChild, rightChild

def main():
    scales = [100, 1000, 10000, 100000]
    
    for n in scales:
        if random.random() < 0.5:
            leftChild, rightChild = generate_valid_tree(n)
        else:
            leftChild, rightChild = generate_invalid_tree(n)
            
        # Write individual files to avoid huge json payload
        out_path = os.path.join(os.path.dirname(__file__), f"data_{n}.json")
        with open(out_path, "w") as f:
            json.dump({
                "n": n,
                "leftChild": leftChild,
                "rightChild": rightChild
            }, f)
        print(f"Generated data for n={n}")
        
if __name__ == "__main__":
    main()
