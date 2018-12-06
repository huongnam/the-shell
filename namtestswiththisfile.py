#!/usr/bin/env python3
from os import chdir, environ, getcwd, path
from subprocess import run
from history import *
from path_expansions import path_expansions
import re
from shlex import split
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
    _path = None
    # if args is more than 1 -> path is the last argument
    if check_args(cd_args):
        _path = cd_args[1]
    if _path:
        if _path is '..':
            change_dir('..')
        else:
            try:
                change_dir(path.abspath(_path))
            except FileNotFoundError:
                print(print_error(_path + ': ', "No such file or"
                      " directory", "cd: "))
    else:  # if len path is 1 -> jump to HOME
        if 'HOME' in environ:
            change_dir(environ['HOME'])
        else:
            print(print_error("", "HOME not set", "cd: "))


def printenv(printenv_args):
    # if len type_in is 1 -> print all the environment
    if not check_args(printenv_args):
        for key in environ.keys():
            print(key + '=' + environ[key])
    else:  # print the value of the key(printenv_args[1])
        if printenv_args[1] in environ.keys():
            print(environ[printenv_args[1]])


def export(export_args):
    if check_args(export_args):
        variables = export_args[1:]
        for variable in variables:
            if '=' not in variable:
                environ[variable] = ''
            else:
                variable = variable.split('=')
                environ[variable[0]] = variable[1]


def unset(unset_args):
    if check_args(unset_args):
        variables = unset_args[1:]
        for variable in variables:
            if variable in environ.keys():
                del environ[variable]


def sh_exit(exit_args):
    if check_args(exit_args):
        if exit_args[1].isdigit():
            print('exit ' + ' '.join(type_in[1:]))
        else:
            print('exit\nintek-sh: exit: ' + ' '.join(type_in[1:]))
    else:
        print('exit')


def run_file(file_args):
    check = False
    if './' in file_args[0]:
        try:
            run(file_args[0])
        except PermissionError:
            print(print_error(file_args[0], ": Permission denied"))
        except FileNotFoundError:
            print(print_error(file_args[0], ": No such file or directory"))
    else:
        try:
            # find all the possible paths
            PATH = environ['PATH'].split(':')
        except KeyError as e:
            print(print_error(file_args[0], ": command not found"))
            return e
        for item in PATH:
            if path.exists(item+'/'+file_args[0]):
                run([item+'/'+file_args.pop(0)]+file_args)
                check = True
                break
        if not check:  # if the command didn't run
            print(print_error(file_args[0], ": command not found"))


def print_error(arg, _error, _cd=''):
    return "intek-sh: " + _cd + arg + _error


def process_function(functions, command, args):
    functions[command](args)
    if 'exit' in command:
        return False
    else:
        return True

#
# def QuoteForPOSIX(string):
#     return "\\'".join("'" + i + "'" for i in string.split("'"))


def handle_input(_args):
    type_in = []
    _args = split(_args)

    for element in _args:
        if element:
            if '~' in element or '$' in element:
                string = path_expansions(element)
                type_in.append(string)
            else:
                type_in.append(element)
    return type_in


def main():
    global type_in
    flag = True
    special_cases = ['! ', '!', '!=']
    history_lst = []
    functions = {
            'cd': cd,
            'printenv': printenv,
            'export': export,
            'unset': unset,
            'exit': sh_exit,
            'history': print_history
            }
    while flag:
        try:
            _args = input('\033[92m\033[1mintek-sh$\033[0m ')
            # expand history_file
            if not _args.startswith('!') and _args not in special_cases:
                if '!#' not in _args and '^' not in _args:
                    write_history_file(_args)

            # get args and check existence
            history_lst = read_history_file()
            args, exist, hashtag_flag = handle_command(_args, history_lst)

            # when to continue or pass
            continue_flag, pass_flag, args = handle_special_case(exist, args)
            if continue_flag:
                continue
            elif pass_flag:
                pass

            type_in = handle_input(args)
            if type_in:
                if type_in[0] in functions.keys():
                    if 'history' in type_in[0]:
                        history_lst = read_history_file()
                        flag = process_function(functions, type_in[0],
                                                history_lst)
                    else:
                        flag = process_function(functions, type_in[0], type_in)
                else:
                    run_file(type_in)
        except BaseException:
            print('\nintek-sh: muahahahahahahahaaaaaaa')
            continue


if __name__ == '__main__':
        main()
