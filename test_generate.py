from benchmark.lc_1424.generate import generate_data

for n in [100, 1000, 10000]:
    data = generate_data(n)
    total_len = sum(len(row) for row in data)
    print(f"n={n}, total_len={total_len}, rows={len(data)}")
    assert total_len == n
