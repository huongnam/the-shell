#!/usr/bin/env python3
from os import chdir, environ, getcwd, path
from subprocess import run
from history import write_history_file, read_history_file, print_history
from history import handle_command, handle_special_case


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
        elif _path is '~':
            if 'HOME' in environ:
                change_dir(environ['HOME'])
            else:
                change_dir(environ['XAUTHORITY'].strip('.Xauthority'))
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


def handle_input(_args):
    _args = _args.split(' ')
    type_in = []
    for element in _args:
        if element:
            type_in.append(element)
    return type_in


def get_args(curpath, _args):
    if path.exists(curpath + '/.intek-sh_history'):
        history_lst = read_history_file(curpath)
    else:
        print('intek-sh: there\'s nothing in the history list!')
        return None, False
    args, exist = handle_command(_args, history_lst)
    return args, exist


def main():
    global type_in
    curpath = environ['PWD']
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
            hist_written = False
            _args = input('\033[92m\033[1mintek-sh$\033[0m ')
            # expand history_file
            hist_written = expand_history_file(_args, special_cases, curpath)

            # get args and check existence
            args, exist = get_args(curpath, _args)
            if not args and not exist:
                continue
            if not written and not args.startswith('!'):
                write_history_file(args, curpath)

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
                        history_lst = read_history_file(curpath)
                        flag = process_function(functions, type_in[0],
                                                history_lst)
                    else:
                        flag = process_function(functions, type_in[0], type_in)
                else:
                    run_file(type_in)
        except BaseException:
            print('\nintek-sh: something went wrong...')
            continue


if __name__ == '__main__':
    main()
