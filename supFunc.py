from statistics import stdev

def avg(lst):
    return sum(lst)/len(lst)


def normalize(lst):
    average = avg(lst)
    result = []
    dev = stdev(lst)
    for item in lst:
        result.append((item-average)/dev)
    return result


