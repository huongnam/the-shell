#!/usr/bin/env python3
from os import chdir, environ, getcwd, path
from subprocess import run
from exit_status import get_exit_status


'''
cd      : change directory
printenv: print all or part of environment
export  : mark each name to be passed to child processes in the environment
unset   : remove each variable or function name
exit    : end process
'''


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
    global exit_code
    _path = None
    # if args is more than 1 -> path is the last argument
    if check_args(cd_args):
        _path = cd_args[1]
    if _path:
        if _path is '..':
            change_dir('..')
            environ['EXITCODE'] = '0'
        else:
            try:
                change_dir(path.abspath(_path))
                environ['EXITCODE'] = '0'
            except FileNotFoundError:
                print(print_error(_path + ': ', "No such file or"
                      " directory", "cd: "))
                environ['EXITCODE'] = '1'
    else:  # if len path is 1 -> jump to HOME
        if 'HOME' in environ:
            change_dir(environ['HOME'])
            environ['EXITCODE'] = '0'
        else:
            print(print_error("", "HOME not set", "cd: "))
            environ['EXITCODE'] = '1'


def printenv(printenv_args):
    # if len type_in is 1 -> print all the environment
    if not check_args(printenv_args):
        environ['EXITCODE'] = '0'
        for key in environ.keys():
            print(key + '=' + environ[key])
    else:  # print the value of the key(printenv_args[1])
        if printenv_args[1] in environ.keys():
            environ['EXITCODE'] = '0'
            print(environ[printenv_args[1]])
        else:
            environ['EXITCODE'] = '1'


def export(export_args):
    if check_args(export_args):
        variables = export_args[1:]
        for variable in variables:
            if '=' not in variable:
                environ[variable] = ''
                environ['EXITCODE'] = '0'
            else:
                variable = variable.split('=')
                environ[variable[0]] = variable[1]
                environ['EXITCODE'] = '0'


def unset(unset_args):
    if check_args(unset_args):
        variables = unset_args[1:]
        for variable in variables:
            if variable in environ.keys():
                del environ[variable]
                environ['EXITCODE'] = '0'


def sh_exit(exit_args):
    if check_args(exit_args):
        if exit_args[1].isdigit():
            print('exit ' + ' '.join(exit_args[1:]))
            environ['EXITCODE'] = ' '.join(exit_args[1:])
        else:
            print('exit\nintek-sh: exit: ' + ' '.join(exit_args[1:]))
            environ['EXITCODE'] = '0'
    else:
        print('exit')
        environ['EXITCODE'] = '0'


def run_file(file_args):
    check = False
    if './' in file_args[0]:
        try:
            child = run(file_args[0])
            environ['EXITCODE'] = str(child.returncode)
        except PermissionError:
            print(print_error(file_args[0], ": Permission denied"))
            environ['EXITCODE'] = '2'
        except FileNotFoundError:
            print(print_error(file_args[0], ": No such file or directory"))
            environ['EXITCODE'] = '127'
    else:
        try:
            # find all the possible paths
            PATH = environ['PATH'].split(':')
        except KeyError as e:
            print(print_error(file_args[0], ": command not found"))
            environ['EXITCODE'] = '127'
            return e
        for item in PATH:
            if path.exists(item+'/'+file_args[0]):
                child = run([item+'/'+file_args.pop(0)]+file_args)
                environ['EXITCODE'] = str(child.returncode)
                check = True
                break
        if not check:  # if the command didn't run
            print(print_error(file_args[0], ": command not found"))
            environ['EXITCODE'] = '127'


def print_error(arg, _error, _cd=''):
    return "intek-sh: " + _cd + arg + _error


def process_function(functions, command, args):
    functions[command](args)
    if 'exit' in command:
        return False
    else:
        return True


def handle_input(_args):
    _args = _args.split(' ')
    type_in = []
    replace_things = []
    for element in _args:
        if element:
            # exit status
            if '$?' in element or '${?}' in element:
                replace_things = get_exit_status(element)
            else:
                type_in.append(element)
    if replace_things:
        type_in += replace_things
    return type_in


def main():
    flag = True
    environ['EXITCODE'] = '0'
    special_cases = ['! ', '!', '!=']
    history_lst = []
    functions = {
            'cd': cd,
            'printenv': printenv,
            'export': export,
            'unset': unset,
            'exit': sh_exit
            }
    while flag:
        _args = input('\033[92m\033[1mintek-sh$\033[0m ')
        type_in = handle_input(_args)
        if type_in:
            if type_in[0] in functions.keys():
                flag = process_function(functions, type_in[0], type_in)
            else:
                run_file(type_in)


if __name__ == '__main__':
    main()
