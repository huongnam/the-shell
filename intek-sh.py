#!/usr/bin/env python3
from history import write_history_file, read_history_file, print_history
from history import handle_command, handle_special_case, expand_history_file
from exit_status import get_exit_status
from dynamic import make_subcommand_completer
from readline import parse_and_bind, set_completer, set_completer_delims
from os import environ, listdir, path
from signal import signal, SIGINT, SIGTERM, SIGQUIT, SIG_IGN, SIGTSTP
from sys import exit
from builtins_package.process_cd import cd
from builtins_package.process_exit import sh_exit
from builtins_package.process_export import export
from builtins_package.process_printenv import printenv
from builtins_package.process_run_file import run_file
from builtins_package.process_unset import unset


'''
cd      : change directory
printenv: print all or part of environment
export  : mark each name to be passed to child processes in the environment
unset   : remove each variable or function name
exit    : end process
'''


def handle_interrupt(signum, frame):
    ''' KeyboardInterrupt's exit_code: 130'''
    global exit_code
    exit_code = 130
    raise KeyboardInterrupt


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


def get_all_cmds():
    if 'PATH' in environ.keys():
        for cmd_path in environ['PATH'].split(':'):
            try:
                cmds = listdir(cmd_path)
            except FileNotFoundError:
                continue
            for cmd in cmds:
                commands.add(cmd)


def main():
    global type_in
    global exit_code
    global commands
    exit_code = 0
    flag = True
    curpath = environ['PWD']
    special_cases = ['! ', '!', '!=']
    commands = {'history', 'cd', 'printenv', 'export', 'unset', 'exit'}
    history_lst = []
    functions = {
            'cd': cd,
            'printenv': printenv,
            'export': export,
            'unset': unset,
            'exit': sh_exit,
            'history': print_history
            }
    try:
        while flag:
            ''' Ctrl + C '''
            signal(SIGINT, handle_interrupt)

            ''' Ctrl + "\" '''
            signal(SIGQUIT, SIG_IGN)

            ''' the signal that is sent by default by the kill, pkill,
            killall, fuser -k... commands'''
            signal(SIGTERM, SIG_IGN)

            ''' Ctrl + Z '''
            signal(SIGTSTP, SIG_IGN)

            # get all the command in environment PATH
            get_all_cmds()

            parse_and_bind('tab: complete')
            set_completer(make_subcommand_completer(commands))
            set_completer_delims(" \t")

            hist_written = False
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
                    if 'history' in type_in[0]:
                        history_lst = read_history_file(curpath)
                        exit_code = print_history(type_in, history_lst)
                        flag = True
                    else:
                        flag, exit_code = process_function(functions, command,
                                                           type_in)
                else:
                    exit_code = run_file(type_in)
    except KeyboardInterrupt:
        print('^C')
        main()
    except EOFError:
        print()
        exit(0)


if __name__ == '__main__':
    main()
