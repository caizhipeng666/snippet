def czp_slice(data, length):
    for i in range(0, len(data), length):
        yield data[i:i+length]


data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for c in czp_slice(data, 4):
    print(c)
