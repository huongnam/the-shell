#!/usr/bin/env python3
from shlex import split
from history import write_history_file, read_history_file, print_history
from history import handle_command, handle_special_case
from exit_status import get_exit_status
from builtin import *


'''
cd      : change directory
printenv: print all or part of environment
export  : mark each name to be passed to child processes in the environment
unset   : remove each variable or function name
exit    : end process
'''


def process_function(functions, command, args):
    exit_code = functions[command](args)
    if 'exit' in command:
        return False, exit_code
    else:
        return True, exit_code


def handle_input(_args, exit_code):
    type_in = []
    replace_things = []
    _args = split(_args)
    for element in _args:
        if element:
            # exit status
            if '$?' in element or '${?}' in element:
                replace_things = get_exit_status(element, str(exit_code))
            else:
                type_in.append(element)
    if replace_things:
        type_in += replace_things
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
    global exit_code
    exit_code = 0
    flag = True
    curpath = environ['PWD']
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
            written = False
            _args = input('\033[92m\033[1mintek-sh$\033[0m ')

            # expand history_file
            if not _args.startswith('!') and _args not in special_cases:
                if '!#' not in _args and '^' not in _args:
                    write_history_file(_args, curpath)
                    written = True

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

            type_in = handle_input(args, exit_code)
            if type_in:
                command = type_in[0]
                if command in functions.keys():
                    if 'history' in command:
                        history_lst = read_history_file(curpath)
                        flag = process_function(functions, command,
                                                history_lst)
                    else:
                        flag, exit_code = process_function(functions, command,
                                                           type_in)
                else:
                    exit_code = run_file(type_in)
        except BaseException:
            print('intek-sh: sorry thing went wrong...')
            continue


if __name__ == '__main__':
    main()
