# Benchmark Audit

## Summary

- Total benchmark folders: 71
- Clean benchmarks: 60
- Flagged benchmarks: 11

## Topics

- Backtracking: 10 total, 7 clean
- Binary Search: 7 total, 6 clean
- Dynamic Programming: 6 total, 5 clean
- Graph: 10 total, 8 clean
- Heap: 9 total, 9 clean
- Sliding Window: 10 total, 10 clean
- Tree: 6 total, 6 clean
- Two Pointers: 10 total, 9 clean
- UNKNOWN: 3 total, 0 clean

## Flag Counts

- `complexity_label_mismatch`: 2
- `extrapolated_100k`: 6
- `missing_metadata`: 3

## Recommended Validation Sample

- Backtracking: `lc_1593` (Split a String Into the Max Number of Unique Substrings, 100k=8.20ms), `lc_113` (Path Sum II, 100k=51.01ms)
- Binary Search: `lc_1201` (Ugly Number III, 100k=0.67ms), `lc_1038` (Binary Search Tree to Greater Sum Tree, 100k=19.89ms)
- Dynamic Programming: `lc_1014` (Best Sightseeing Pair, 100k=19.56ms), `lc_1024` (Video Stitching, 100k=272.44ms)
- Graph: `lc_1311` (Get Watched Videos by Your Friends, 100k=58.97ms), `lc_1319` (Number of Operations to Make Network Connected, 100k=359.94ms)
- Heap: `lc_1338` (Reduce Array Size to The Half, 100k=20.00ms), `lc_1405` (Longest Happy String, 100k=57.64ms)
- Sliding Window: `lc_1248` (Count Number of Nice Subarrays, 100k=66.00ms), `lc_1004` (Max Consecutive Ones III, 100k=179.04ms)
- Tree: `lc_107` (Binary Tree Level Order Traversal II, 100k=15.24ms), `lc_102` (Binary Tree Level Order Traversal, 100k=15.59ms)
- Two Pointers: `lc_142` (Linked List Cycle II, 100k=4.64ms), `lc_143` (Reorder List, 100k=8.64ms)
- UNKNOWN: no clean benchmarks available

## Flagged Benchmarks

- `lc_1079` | Letter Tile Possibilities | Backtracking | `extrapolated_100k`
  - extrapolated_100k: mapped down to
- `lc_1219` | Path with Maximum Gold | Backtracking | `extrapolated_100k`
  - extrapolated_100k: extrapolat
- `lc_1238` | Circular Permutation in Binary Representation | Backtracking | `extrapolated_100k`
  - extrapolated_100k: mapped n values
- `lc_1027` | Longest Arithmetic Subsequence | Binary Search | `complexity_label_mismatch`
  - complexity_label_mismatch: median log10 deviation=0.73; worst step 10000->100000 actual=1.42x expected=10.00x for O(N)
- `lc_1039` | Minimum Score Triangulation of Polygon | Dynamic Programming | `extrapolated_100k`
  - extrapolated_100k: astronomical amount of time, map the large n values
- `lc_1334` | Find the City With the Smallest Number of Neighbors at a Threshold Distance | Graph | `extrapolated_100k`
  - extrapolated_100k: extrapolat
- `lc_1361` | Validate Binary Tree Nodes | Graph | `complexity_label_mismatch`
  - complexity_label_mismatch: median log10 deviation=0.87; worst step 10000->100000 actual=87.90x expected=10.00x for O(N)
- `lc_15` | 3Sum | Two Pointers | `extrapolated_100k`
  - extrapolated_100k: extrapolat, skip n=100000, too slow
- `lc_1011` | missing title | UNKNOWN | `missing_metadata`
  - missing_metadata: title, topic, notes
- `lc_1049` | missing title | UNKNOWN | `missing_metadata`
  - missing_metadata: title, topic, notes
- `lc_105` | missing title | UNKNOWN | `missing_metadata`
  - missing_metadata: title, topic, notes

## Clean Benchmarks

- `lc_113` | Path Sum II | Backtracking | 100k=51.01ms
- `lc_1239` | Maximum Length of a Concatenated String with Unique Characters | Backtracking | 100k=1081.17ms
- `lc_1286` | Iterator for Combination | Backtracking | 100k=471.97ms
- `lc_131` | Palindrome Partitioning | Backtracking | 100k=739.11ms
- `lc_1415` | The k-th Lexicographical String of All Happy Strings of Length n | Backtracking | 100k=292.85ms
- `lc_1593` | Split a String Into the Max Number of Unique Substrings | Backtracking | 100k=8.20ms
- `lc_17` | Letter Combinations of a Phone Number | Backtracking | 100k=42533.02ms
- `lc_1008` | Construct Binary Search Tree from Preorder Traversal | Binary Search | 100k=264.84ms
- `lc_1038` | Binary Search Tree to Greater Sum Tree | Binary Search | 100k=19.89ms
- `lc_109` | Convert Sorted List to Binary Search Tree | Binary Search | 100k=102.71ms
- `lc_1146` | Snapshot Array | Binary Search | 100k=1179.13ms
- `lc_1170` | Compare Strings by Frequency of the Smallest Character | Binary Search | 100k=27.52ms
- `lc_1201` | Ugly Number III | Binary Search | 100k=0.67ms
- `lc_1014` | Best Sightseeing Pair | Dynamic Programming | 100k=19.56ms
- `lc_1024` | Video Stitching | Dynamic Programming | 100k=272.44ms
- `lc_1035` | Uncrossed Lines | Dynamic Programming | 100k=784.20ms
- `lc_1043` | Partition Array for Maximum Sum | Dynamic Programming | 100k=3910.39ms
- `lc_1105` | Filling Bookcase Shelves | Dynamic Programming | 100k=827.15ms
- `lc_1042` | Flower Planting With No Adjacent | Graph | 100k=1404.90ms
- `lc_1129` | Shortest Path with Alternating Colors | Graph | 100k=1880.03ms
- `lc_1311` | Get Watched Videos by Your Friends | Graph | 100k=58.97ms
- `lc_1319` | Number of Operations to Make Network Connected | Graph | 100k=359.94ms
- `lc_133` | Clone Graph | Graph | 100k=792.68ms
- `lc_1462` | Course Schedule IV | Graph | 100k=3714.90ms
- `lc_1466` | Reorder Routes to Make All Paths Lead to the City Zero | Graph | 100k=1253.43ms
- `lc_1514` | Path with Maximum Probability | Graph | 100k=3076.67ms
- `lc_1054` | Distant Barcodes | Heap | 100k=543.99ms
- `lc_1094` | Car Pooling | Heap | 100k=788.89ms
- `lc_1268` | Search Suggestions System | Heap | 100k=187.66ms
- `lc_1338` | Reduce Array Size to The Half | Heap | 100k=20.00ms
- `lc_1353` | Maximum Number of Events That Can Be Attended | Heap | 100k=635.30ms
- `lc_1405` | Longest Happy String | Heap | 100k=57.64ms
- `lc_1424` | Diagonal Traverse II | Heap | 100k=315.79ms
- `lc_1438` | Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit | Heap | 100k=1612.34ms
- `lc_1488` | Avoid Flood in The City | Heap | 100k=132.02ms
- `lc_1004` | Max Consecutive Ones III | Sliding Window | 100k=179.04ms
- `lc_1016` | Binary String With Substrings Representing 1 To N | Sliding Window | 100k=3211.98ms
- `lc_1031` | Maximum Sum of Two Non-Overlapping Subarrays | Sliding Window | 100k=580.56ms
- `lc_1040` | Moving Stones Until Consecutive II | Sliding Window | 100k=1053.67ms
- `lc_1052` | Grumpy Bookstore Owner | Sliding Window | 100k=385.97ms
- `lc_1156` | Swap For Longest Repeated Character Substring | Sliding Window | 100k=291.88ms
- `lc_1208` | Get Equal Substrings Within Budget | Sliding Window | 100k=1035.12ms
- `lc_1234` | Replace the Substring for Balanced String | Sliding Window | 100k=339.99ms
- `lc_1248` | Count Number of Nice Subarrays | Sliding Window | 100k=66.00ms
- `lc_1297` | Maximum Number of Occurrences of a Substring | Sliding Window | 100k=951.70ms
- `lc_102` | Binary Tree Level Order Traversal | Tree | 100k=15.59ms
- `lc_1026` | Maximum Difference Between Node and Ancestor | Tree | 100k=40.95ms
- `lc_103` | Binary Tree Zigzag Level Order Traversal | Tree | 100k=20.01ms
- `lc_106` | Construct Binary Tree from Inorder and Postorder Traversal | Tree | 100k=88.25ms
- `lc_107` | Binary Tree Level Order Traversal II | Tree | 100k=15.24ms
- `lc_1080` | Insufficient Nodes in Root to Leaf Paths | Tree | 100k=276.92ms
- `lc_1023` | Camelcase Matching | Two Pointers | 100k=553.74ms
- `lc_1048` | Longest String Chain | Two Pointers | 100k=3080.31ms
- `lc_11` | Container With Most Water | Two Pointers | 100k=387.85ms
- `lc_1237` | Find Positive Integer Solution for a Given Equation | Two Pointers | 100k=628.59ms
- `lc_142` | Linked List Cycle II | Two Pointers | 100k=4.64ms
- `lc_143` | Reorder List | Two Pointers | 100k=8.64ms
- `lc_1471` | The k Strongest Values in an Array | Two Pointers | 100k=59.70ms
- `lc_148` | Sort List | Two Pointers | 100k=1252.41ms
- `lc_1498` | Number of Subsequences That Satisfy the Given Sum Condition | Two Pointers | 100k=1247.58ms

## Notes

- `complexity_label_mismatch` is based on the 1k->10k and 10k->100k timing ratios versus the declared empirical time complexity.
- `timing_jump_gt_20x_expected` is intentionally conservative and only triggers on extreme blow-ups.
- `extrapolated_100k` is flagged when `bench.py` or `results.json` notes indicate the 100k result was skipped, mapped, or extrapolated rather than directly measured.
