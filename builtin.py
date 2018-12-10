from os import chdir, environ, getcwd, path
from subprocess import run
from sys import exit


# check if args is more than 1
def check_args(args):
    if len(args) is not 1:
        return True
    else:
        return False


# change the path and set environ PWD as the path
def change_dir(dir_path):
    chdir(dir_path)
    environ['PWD'] = getcwd()


def cd(cd_args):
    _path = None
    # if args is more than 1 -> path is the last argument
    if check_args(cd_args):
        _path = cd_args[1]
    if _path:
        if _path is '..':
            change_dir('..')
            exit_code = 0
        else:
            try:
                change_dir(path.abspath(_path))
                exit_code = 0
            except FileNotFoundError:
                print(print_error(_path + ': ', "No such file or"
                      " directory", "cd: "))
                exit_code = 1
    else:  # if len path is 1 -> jump to HOME
        if 'HOME' in environ:
            change_dir(environ['HOME'])
            exit_code = 0
        else:
            print(print_error("", "HOME not set", "cd: "))
            exit_code = 1
    return exit_code


def printenv(printenv_args):
    # if len type_in is 1 -> print all the environment
    exit_code = None
    if not check_args(printenv_args):
        exit_code = 0
        for key in environ.keys():
            print(key + '=' + environ[key])
    else:  # print the value of the key(printenv_args[1])
        if printenv_args[1] in environ.keys():
            exit_code = 0
            print(environ[printenv_args[1]])
        else:
            exit_code = 1
    return exit_code


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


def unset(unset_args):
    exit_code = None
    if check_args(unset_args):
        variables = unset_args[1:]
        for variable in variables:
            if variable in environ.keys():
                del environ[variable]
                exit_code = 0
    return exit_code


def sh_exit(exit_args):
    if check_args(exit_args):
        if exit_args[1].isdigit():
            print('exit ' + ' '.join(exit_args[1:]))
            exit_code = int(' '.join(exit_args[1:]))
        else:
            print('exit\nintek-sh: exit: ' + ' '.join(exit_args[1:]))
            exit_code = 0
    else:
        print('exit')
        exit_code = 0
    exit(exit_code)


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


def print_error(arg, _error, _cd=''):
    return "intek-sh: " + _cd + arg + _error
