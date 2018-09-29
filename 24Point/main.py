def calc(ops, a, b):
    c = None
    if (ops == '+'):
        c = a + b
    elif (ops == '-'):
        c = a - b
    elif (ops == '*'):
        c = a * b
    elif (ops == '/' and b != 0):
        c = a / b
    else:
        print("ValueError : ops = {}, a= {}, b = {}".format(ops, a, b))
    return c

def formatAns(ret):
    ret = '(((', ret[0], ret[2], ret[1],')', ret[5], ret[4],')', ret[8], ret[7], ')'
    return ''.join([str(i) for i in ret])


def getKey(ops, a, b, parent_ops_str_key, n):
    '''
    It's can work only when variable a and b are small num( < 58)
    '''
    s = '+-*/'
    o = s.find(ops)
    if (o == -1):
        print("KeyError ops must in {+-*/}")
        return None

    key = 0
    if (a < 0):
        a -= a
        key |= 1
    if (b < 0):
        b -= b
        key |= 2

    key |= 1 << (a + 6)
    key |= 1 << (b + 6)
    key |= 1 << (o + 2)
    return (key ^ parent_ops_str_key) << n


def getKey2(child_ops):
    return ''.join([str(c) for c in child_ops])


POINT = 24


def getSoulation(candidate, ret, record):
    close = set()

    while candidate:
        c_list = candidate.popitem()
        last_ans = c_list[0]

        for cur in c_list[1]:
            parent_ops_key, parent_ops, parent_open_list, parent_key = cur

            for b in parent_open_list:
                for ch_ops in '+-*/':
                    child_ops = parent_ops.copy() + [last_ans, b, ch_ops]
                    ops_key = getKey(ch_ops, last_ans, b, parent_ops_key, len(parent_open_list) - 1)
                    # ops_key = getKey(child_ops)
                    if ops_key in close:
                        continue
                    close.add(ops_key)

                    ans = calc(ch_ops, last_ans, b)
                    if not ans:
                        # print("ValueError: divided by zero !")
                        continue
                    if ans != int(ans):
                        continue
                    ans = int(ans)
                    sub_open = parent_open_list.copy()
                    sub_open.remove(b)


                    info = [ops_key, child_ops, sub_open, parent_ops_key]
                    if ans not in candidate:
                        candidate[ans] = list()

                    candidate[ans].append(info)

                    if ans not in record:
                        record[ans] = list()
                    record[ans].append(info)

                    if (ans == POINT and len(sub_open) == 0):
                        ret.append(child_ops)

import copy

def game24(open_list=[5, 7, 3, 2], show_record=False):
    ret = []
    record = {}
    # ans : [ops_key, ops, open, parent_ops_key]
    pattern = [0, [], open_list, 0]

    candidate = {}

    for e in open_list:
        if e not in candidate:
            candidate[e] = []
        tmp = copy.deepcopy(pattern)
        tmp[2].remove(e)
        candidate[e].append(tmp)

    getSoulation(candidate, ret, record)

    def show_info(record):
        for k, val in record.items():
            print("ans = {}".format(k))
            for v in val:
                print(v)

    if (show_record):
        show_info(record)

    print("answer:")
    if ret:
        for i, r in enumerate(ret):
            #print(r)
            r = formatAns(r)
            print(i,' ',r)

    else:
        print("No answer")
    return ret

ret = game24([24, 1, 1, 1])

print("------check----------")
sorted_ret = []
for r in ret:
    r = [[r[i * 3], r[i * 3 + 1], r[i * 3 + 2]] for i in range(3)]
    # print(r)
    r = [' '.join([str(j) for j in i]) for i in r]
    sorted_ret.append(r)

sorted_ret.sort()
for i, r in enumerate(sorted_ret):
    print(i, ' ',r)