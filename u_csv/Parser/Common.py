nl = '<br>'


def ListToStr(l: list, delimiter: str = ', ', end: str = '.', func=str) -> str:
    L = len(l)
    if L == 0:
        return '<empty list>' + end
    out = func(l[0])
    for i in range(1, L):
        out += delimiter + func(l[i])
    return out + end
