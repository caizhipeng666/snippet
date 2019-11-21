import itertools


def czp_slice(data, length):
    for i in range(0, len(data), length):
        yield data[i:i+length]


czp_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for c in czp_slice(czp_data, 4):
    print(c)


def chunk(iterable, iter_size, is_fill=False, filler=None):
    """
    迭代块访问
    :param iterable: 可迭代对象
    :param iter_size: 每次迭代大小
    :param is_fill: 切块不够, 是否填充
    :param filler: 填充对象
    """
    fill_size = iter_size - 1 if is_fill else 0
    it = itertools.chain(iterable, itertools.repeat(filler, fill_size))
    chunk = tuple(itertools.islice(it, iter_size))
    while len(chunk) == iter_size:
        yield chunk
        chunk = tuple(itertools.islice(it, iter_size))
