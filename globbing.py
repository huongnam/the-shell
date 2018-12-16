#!/usr/bin/env python3
from glob import glob
from itertools import product


def pre_glob(pattern):
    return [i+1 for i in range(len(pattern)) if pattern.startswith('.*', i)]


def do_globbing(pattern):
    out = glob(pattern)
    result = set(out)

    # case .? / .?*
    if pattern.startswith('.?') and '/' not in pattern:
        result.add('..')

    # case .*/.*
    if '.*' in pattern:
        dot_asterisk_num = pattern.count('.*')

        # list all indexes of '*' of '.*' in pattern
        dot_asterisk_idxs = pre_glob(pattern)

        # make a list of tuple ~ [('', ''), ('', '.'), ('', '*'),..]
        cases = list(product(['', '.', '*'], repeat=dot_asterisk_num))

        # change pattern to list ~ ['.', '*', '/', '.', '*']
        pattern = list(pattern)

        for case in cases:
            for i in range(dot_asterisk_num):
                # turn .* to ./ ../ .*
                pattern[dot_asterisk_idxs[i]] = case[i]
                result.update(glob(''.join(pattern)))
    return list(result)
