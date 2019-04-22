def gen_spongebob_mock(s):
    new_s = ""
    flag = False
    for c in s:
        if flag:
            new_s += c.upper()
        else: 
            new_s += c.lower()
        flag = not flag
    return new_s
