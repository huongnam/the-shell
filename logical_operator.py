from namtestswiththisfile import dep

def split_operator(args, operator):
    args = args.split(sep=operator)
    return args


def handle_and(args, functions):
    exit_code = 0
    for item in args:
        if exit_code == 0:
            flag, exit_code = dep(item, functions)


def handle_or(args, functions):
    exit_code = None
    for item in args:
        while exit_code != 0:
            flag, exit_code = dep(item, functions)
            break

def handle_logical_operator(args, functions):
    _args = args
    if "&&" in _args:
        _args = split_operator(_args, "&&")
        handle_and(_args, functions)
    if "||" in _args:
        _args = split_operator(_args, "||")
        handle_or(_args, functions)
