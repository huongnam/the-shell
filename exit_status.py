from os import environ


def get_exit_status(arg):
    replace_things = []
    if '$?' in arg:
        arg = arg.replace('$?', environ['EXITCODE'])
        replace_things.append(arg)
    elif '${?}' in arg:
        arg = arg.replace('${?}', environ['EXITCODE'])
        replace_things.append(arg)
    return replace_things
