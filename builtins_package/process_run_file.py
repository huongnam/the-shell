from subprocess import run
from os import environ, path


def print_error(arg, _error, _cd=''):
    return "intek-sh: " + _cd + arg + _error


def run_file(file_args):
    check = False
    exit_code = None
    if './' in file_args[0]:
        try:
            child = run(file_args[0])
            exit_code = child.returncode
        except PermissionError:
            print(print_error(file_args[0], ": Permission denied"))
            exit_code = 2
        except FileNotFoundError:
            print(print_error(file_args[0], ": No such file or directory"))
            exit_code = 127
    else:
        try:
            # find all the possible paths
            PATH = environ['PATH'].split(':')
        except KeyError as e:
            print(print_error(file_args[0], ": command not found"))
            exit_code = 127
            return e
        for item in PATH:
            if path.exists(item+'/'+file_args[0]):
                child = run([item+'/'+file_args.pop(0)]+file_args)
                exit_code = child.returncode
                check = True
                break
        if not check:  # if the command didn't run
            print(print_error(file_args[0], ": command not found"))
            exit_code = 127
    return exit_code
