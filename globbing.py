from glob import glob


def do_globbing(thing_to_glob):
    list = glob(thing_to_glob)
    # give it some upgrade
    if '/' in thing_to_glob and\
            thing_to_glob[thing_to_glob.rfind('/') + 1] == '*':
        list += [thing_to_glob.strip('*') + '.',
                 thing_to_glob.strip('*') + '..']
    elif thing_to_glob is '*':
        list += ['.', '..']
    list.sort()
    return list
