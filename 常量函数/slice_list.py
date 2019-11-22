import itertools


def czp_slice(data, length):
    for i in range(0, len(data), length):
        yield data[i:i + length]


def grouped(iterable, n):
    """
    (s0,s1,s2,...sn-1),
    (sn,sn+1,sn+2,...s2n-1)
    (s2n,s2n+1,s2n+2,...s3n-1)
    缺点: 按最小分片操作, 可能最后会漏
    """
    return zip(*[iter(iterable)] * n)


def chunk(iterable, iter_size, is_fill=False, filler=None):
    """
    迭代块访问
    iterable: 可迭代对象
    iter_size: 每次迭代大小
    is_fill: 切块不够, 是否填充
    filler: 填充对象
    """
    fill_size = iter_size - 1 if is_fill else 0
    it = itertools.chain(iterable, itertools.repeat(filler, fill_size))
    chunk = tuple(itertools.islice(it, iter_size))
    while len(chunk) == iter_size:
        yield chunk
        chunk = tuple(itertools.islice(it, iter_size))
