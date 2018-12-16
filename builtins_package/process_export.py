from os import environ


# check if args is more than 1
def check_args(args):
    if len(args) is not 1:
        return True
    else:
        return False


def export(export_args):
    exit_code = None
    if check_args(export_args):
        variables = export_args[1:]
        for variable in variables:
            if '=' not in variable:
                environ[variable] = ''
                exit_code = 0
            else:
                variable = variable.split('=')
                environ[variable[0]] = variable[1]
                exit_code = 0
    return exit_code
