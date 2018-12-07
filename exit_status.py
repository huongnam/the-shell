from os import environ


def get_exit_status(arg, exit_code):
    replace_things = []
    if '$?' in arg:
        arg = arg.replace('$?', exit_code)
        replace_things.append(arg)
    elif '${?}' in arg:
        arg = arg.replace('${?}', exit_code)
        replace_things.append(arg)
    return replace_things
