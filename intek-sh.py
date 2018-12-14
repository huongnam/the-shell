#!/usr/bin/env python3
from shlex import split
from history import write_history_file, read_history_file, print_history
from history import handle_command, handle_special_case, expand_history_file
from exit_status import get_exit_status
from builtin import *
from glob import glob
from readline import parse_and_bind, set_completer, set_completer_delims
from readline import read_history_file as rdline_read
from dynamic import make_subcommand_completer
from os import listdir


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
    _args = _args.split()
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
        raise FileNotFoundError
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
    commands = {'ls', 'history', 'cd', 'printenv', 'export', 'unset', 'exit'}
    for cmd_path in environ['PATH'].split(':'):
        try:
            cmds = listdir(cmd_path)
        except FileNotFoundError:
            continue
        for cmd in cmds:
            commands.add(cmd)
    functions = {
            'cd': cd,
            'printenv': printenv,
            'export': export,
            'unset': unset,
            'exit': sh_exit,
            'history': print_history
            }
    while flag:
        # try:
        hist_written = False
        histfile = curpath + '/.intek-sh_history'
        parse_and_bind('tab: complete')
        set_completer(make_subcommand_completer(commands))
        set_completer_delims(" \t\n\"\\'`@$><=;|&{(")
        try:
            rdline_read(histfile)
        except FileNotFoundError:
            pass
        _args = input('\033[92m\033[1mintek-sh$\033[0m ')

        # expand history_file
        history_lst = read_history_file(curpath)
        hist_written = expand_history_file(_args, special_cases, curpath,
                                           history_lst)

        # get args and check existence of _args in history_lst
        args, exist = get_args(curpath, _args)
        # if there is no command typed in so far
        if not args and not exist:
            print('intek-sh: there\'s nothing in the history list')
            continue
        # check if the after args in history_lst
        if not hist_written:
            history_lst = read_history_file(curpath)
            hist_written = expand_history_file(_args, special_cases, curpath,
                                               history_lst)

        # when to continue
        continue_flag, args = handle_special_case(exist, args)
        if continue_flag:
            continue

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
        # except BaseException:
        #     print('intek-sh: muahahahahahahahahaha')
        #     continue


if __name__ == '__main__':
    main()
