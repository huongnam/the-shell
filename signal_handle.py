#!/usr/bin/env python3
from exit_status import get_exit_status
from builtin import *
from signal import signal, SIGINT, SIGTERM, SIGQUIT, SIG_IGN, SIGTSTP
from sys import exit


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


def main():
    global type_in
    global exit_code
    flag = True
    functions = {
            'cd': cd,
            'printenv': printenv,
            'export': export,
            'unset': unset,
            'exit': sh_exit,
            }
    try:
        while flag:
            ''' Ctrl + C '''
            signal(SIGINT, handle_interrupt)

            ''' Ctrl + \ '''
            signal(SIGQUIT, SIG_IGN)

            ''' the signal that is sent by default by the kill, pkill,
            killall, fuser -k... commands'''
            signal(SIGTERM, SIG_IGN)

            ''' Ctrl + Z '''
            signal(SIGTSTP, SIG_IGN)

            _args = input('\033[92m\033[1mintek-sh$\033[0m ')

            type_in = handle_input(_args, exit_code)
            if type_in:
                command = type_in[0]
                if command in functions.keys():
                    flag, exit_code = process_function(functions, command,
                                                       type_in)
                else:
                    exit_code = run_file(type_in)
    except KeyboardInterrupt:
        print()
        main()
    except EOFError:
        print()
        exit(0)


if __name__ == '__main__':
    main()
