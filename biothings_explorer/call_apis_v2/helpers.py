from itertools import islice


def iter_n(iterable, n, with_cnt=False):
    """
    can use itertools.batched for Python 3.12+

    Iterate an iterator by chunks (of n)
    if with_cnt is True, return (chunk, cnt) each time
    ref http://stackoverflow.com/questions/8991506/iterate-an-iterator-by-chunks-of-n-in-python
    """
    it = iter(iterable)
    if with_cnt:
        cnt = 0
    while True:
        chunk = tuple(islice(it, n))
        if not chunk:
            return
        if with_cnt:
            cnt += len(chunk)
            yield (chunk, cnt)
        else:
            yield chunk
