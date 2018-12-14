from os import environ


# check if args is more than 1
def check_args(args):
    if len(args) is not 1:
        return True
    else:
        return False


def unset(unset_args):
    exit_code = None
    if check_args(unset_args):
        variables = unset_args[1:]
        for variable in variables:
            if variable in environ.keys():
                del environ[variable]
                exit_code = 0
    return exit_code
