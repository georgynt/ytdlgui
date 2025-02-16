

def test(int a) -> int:
    cdef int b = 2
    print(a, b)

    return a + b


test(2)
