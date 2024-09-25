def sum_list(li) :
    total =0
    for x in li:
        total += x
    return res

def max_list(li) :
    res = 0
    for x in li:
        if res<x:
            res=x
    return res


def min_list(li):
    res = 0
    for x in li:
        if res > x:
            res = x
    return res

def set_union(s, *sets):
    res = s
    for sett in sets:
        res = res | sett
    return res