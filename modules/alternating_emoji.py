def gen_alternating_emoji(s):
    s = s.strip()
    split_s = s.split()
    if len(s) == 0:
        return ""
    else:
        return "\U0001F44F " + " \U0001F44F ".join(split_s)
